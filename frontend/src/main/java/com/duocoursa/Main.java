package com.duocoursa;

import com.duocoursa.api.ApiClient;
import com.duocoursa.model.CourseResponse;
import org.fusesource.jansi.AnsiConsole;
import static org.fusesource.jansi.Ansi.ansi;

import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // Install Jansi for colored output
        AnsiConsole.systemInstall();
        
        try {
            // Check if backend is running
            if (!ApiClient.checkHealth()) {
                System.out.println(ansi().fgRed().a("Error: Backend service is not running. Please start the FastAPI server first.").reset());
                System.exit(1);
            }

            printHeader();
            CourseResponse course = getUserInputAndGenerateCourse();
            displayCourse(course);
        } catch (Exception e) {
            System.out.println(ansi().fgRed().a("Error: " + e.getMessage()).reset());
        } finally {
            AnsiConsole.systemUninstall();
        }
    }

    private static void printHeader() {
        System.out.println(ansi().fgCyan().bold().a("""
            ╔════════════════════════════════════╗
            ║         Welcome to DuoCoursa        ║
            ║    Personalized Learning Courses    ║
            ╚════════════════════════════════════╝
            """).reset());
    }

    private static CourseResponse getUserInputAndGenerateCourse() throws IOException {
        Scanner scanner = new Scanner(System.in);

        // Get topic
        System.out.print(ansi().fgGreen().a("Enter the topic you want to learn: ").reset());
        String topic = scanner.nextLine().trim();
        while (topic.isEmpty()) {
            System.out.print(ansi().fgRed().a("Topic cannot be empty. Please try again: ").reset());
            topic = scanner.nextLine().trim();
        }

        // Get level
        System.out.print(ansi().fgGreen().a("Enter your current level (Beginner/Intermediate/Advanced): ").reset());
        String level = scanner.nextLine().trim();
        while (!level.matches("(?i)(beginner|intermediate|advanced)")) {
            System.out.print(ansi().fgRed().a("Please enter either Beginner, Intermediate, or Advanced: ").reset());
            level = scanner.nextLine().trim();
        }

        // Get days
        int days = 0;
        boolean validDays = false;
        while (!validDays) {
            System.out.print(ansi().fgGreen().a("Enter the number of days you want to study (1-365): ").reset());
            try {
                days = Integer.parseInt(scanner.nextLine().trim());
                if (days > 0 && days <= 365) {
                    validDays = true;
                } else {
                    System.out.println(ansi().fgRed().a("Please enter a number between 1 and 365.").reset());
                }
            } catch (NumberFormatException e) {
                System.out.println(ansi().fgRed().a("Please enter a valid number.").reset());
            }
        }

        System.out.println(ansi().fgYellow().a("\nGenerating your personalized course plan...").reset());
        return ApiClient.generateCourse(topic, level, days);
    }

    private static void displayCourse(CourseResponse course) {
        // Course Overview
        System.out.println(ansi().fgCyan().bold().a("\n📚 Course Overview").reset());
        System.out.println(ansi().fgYellow().a("Topic: ").reset().toString() + course.topic);
        System.out.println(ansi().fgYellow().a("Level: ").reset().toString() + course.level);
        System.out.println(ansi().fgYellow().a("Duration: ").a(String.valueOf(course.days)).a(" days\n").reset());

        // Modules and Lessons
        System.out.println(ansi().fgCyan().bold().a("📖 Modules and Lessons").reset());
        for (CourseResponse.Module module : course.modules) {
            System.out.println(ansi().fgMagenta().bold().a("\n➤ " + module.name).reset());
            for (CourseResponse.Lesson lesson : module.lessons) {
                System.out.println(ansi().fgYellow().a("  • ").reset() + lesson.title);
                System.out.println("    " + lesson.content);
            }
        }

        // Daily Tasks
        System.out.println(ansi().fgCyan().bold().a("\n✓ Daily Tasks").reset());
        for (String task : course.tasks) {
            System.out.println(ansi().fgYellow().a("  • ").reset() + task);
        }

        // Quizzes
        System.out.println(ansi().fgCyan().bold().a("\n❓ Quizzes").reset());
        for (int i = 0; i < course.quizzes.size(); i++) {
            CourseResponse.Quiz quiz = course.quizzes.get(i);
            System.out.println(ansi().fgYellow().a("\nQuiz ").a(String.valueOf(i + 1)).reset());
            System.out.println("Question: " + quiz.question);
            System.out.println("Options:");
            for (String option : quiz.options) {
                System.out.println("  - " + option);
            }
            String result = course.simulated_quiz_results.get("Quiz " + String.valueOf(i + 1));
            if (result != null) {
                System.out.println(ansi().fgGreen().a("Simulated Result: " + result).reset());
            }
        }

        // Practice Plan
        System.out.println(ansi().fgCyan().bold().a("\n🎯 Practice Plan").reset());
        for (String practice : course.practice_plan) {
            System.out.println(ansi().fgYellow().a("  • ").reset() + practice);
        }

        // Footer
        System.out.println(ansi().fgCyan().bold().a("\n╔════════════════════════════════════╗").reset());
        System.out.println(ansi().fgCyan().bold().a("║   Happy Learning with DuoCoursa!   ║").reset());
        System.out.println(ansi().fgCyan().bold().a("╚════════════════════════════════════╝").reset());
    }
}
