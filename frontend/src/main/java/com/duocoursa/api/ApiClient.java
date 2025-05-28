package com.duocoursa.api;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.duocoursa.model.CourseResponse;

public class ApiClient {
    private static final String API_URL = "http://127.0.0.1:8000/generate-course";
    private static final Gson gson = new Gson();

    public static CourseResponse generateCourse(String topic, String level, int days) throws IOException {
        URL url = new URL(API_URL);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json; utf-8");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoOutput(true);

        // Create JSON payload
        JsonObject jsonInput = new JsonObject();
        jsonInput.addProperty("topic", topic);
        jsonInput.addProperty("level", level);
        jsonInput.addProperty("days", days);

        // Send request
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = gson.toJson(jsonInput).getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        // Handle response
        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                return gson.fromJson(response.toString(), CourseResponse.class);
            }
        } else {
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getErrorStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                throw new IOException("API Error: " + response.toString());
            }
        }
    }

    public static boolean checkHealth() {
        try {
            URL url = new URL("http://127.0.0.1:8000/health");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            return connection.getResponseCode() == HttpURLConnection.HTTP_OK;
        } catch (Exception e) {
            return false;
        }
    }
}
