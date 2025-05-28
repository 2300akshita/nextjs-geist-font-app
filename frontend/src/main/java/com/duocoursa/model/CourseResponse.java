package com.duocoursa.model;

import java.util.List;
import java.util.Map;

public class CourseResponse {
    public String topic;
    public String level;
    public int days;
    public List<Module> modules;
    public List<String> tasks;
    public List<Quiz> quizzes;
    public List<String> practice_plan;
    
    public static class Module {
        public String name;
        public List<Lesson> lessons;
    }
    
    public static class Lesson {
        public String title;
        public String explanation;  // Deep explanation (5-10 lines)
        public String content;
        public String coding_task;  // Specific coding/practice task
        public String key_takeaway;  // Summary of key points
        
        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("Title: ").append(title).append("\n\n");
            sb.append("Explanation:\n").append(explanation).append("\n\n");
            sb.append("Content: ").append(content).append("\n\n");
            sb.append("Coding Task:\n").append(coding_task).append("\n\n");
            sb.append("Key Takeaway: ").append(key_takeaway).append("\n");
            return sb.toString();
        }
    }
    
    public static class Quiz {
        public String question;
        public List<String> options;  // Must have exactly 4 options
        public String correct_answer;
        
        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("Question: ").append(question).append("\n");
            sb.append("Options:\n");
            for (int i = 0; i < options.size(); i++) {
                sb.append((char)('A' + i)).append(") ").append(options.get(i)).append("\n");
            }
            sb.append("Correct Answer: ").append(correct_answer);
            return sb.toString();
        }
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Course Details:\n");
        sb.append("Topic: ").append(topic).append("\n");
        sb.append("Level: ").append(level).append("\n");
        sb.append("Duration: ").append(days).append(" days\n\n");
        
        sb.append("Modules:\n");
        for (int i = 0; i < modules.size(); i++) {
            Module module = modules.get(i);
            sb.append("\nModule ").append(i + 1).append(": ").append(module.name).append("\n");
            
            for (int j = 0; j < module.lessons.size(); j++) {
                sb.append("\nLesson ").append(j + 1).append(":\n");
                sb.append(module.lessons.get(j).toString()).append("\n");
            }
        }
        
        sb.append("\nQuizzes:\n");
        for (int i = 0; i < quizzes.size(); i++) {
            sb.append("\nQuiz ").append(i + 1).append(":\n");
            sb.append(quizzes.get(i).toString()).append("\n");
        }
        
        sb.append("\nPractice Plan:\n");
        for (String plan : practice_plan) {
            sb.append("- ").append(plan).append("\n");
        }
        
        return sb.toString();
    }
}
