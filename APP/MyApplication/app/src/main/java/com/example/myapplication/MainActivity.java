package com.example.myapplication;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.text.Html;
import android.util.Log;

import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import javax.net.ssl.HttpsURLConnection;
import java.net.URL;

import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static final String LOGIN_URL = "https://rise-and-reflect.onrender.com/app_login/";
    Button btnLogin, btn_PostRequest, btn_PutRequest;
    EditText etUsername, etPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize UI elements
        etUsername = findViewById(R.id.etUsername);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);

        btnLogin.setOnClickListener(v -> {
            // Get username and password from EditText fields
            String username = etUsername.getText().toString().trim();
            String password = etPassword.getText().toString().trim();

            Log.d(TAG, "Username: " + username);
            Log.d(TAG, "Password: " + password);

            // Create a JSON object with username and password
            JSONObject jsonPayload = new JSONObject();
            try {
                jsonPayload.put("username", username);
                jsonPayload.put("password", password);
            } catch (JSONException e) {
                Log.d(TAG, "Json creation failed");
                e.printStackTrace();
            }

            // Execute the login task
            new LoginTask().execute(jsonPayload.toString());
        });
    }

    private class LoginTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {
            String payload = params[0];
            Log.d(TAG, "Payload: " + payload);
            String response = "";

            try {
                // Create URL object
                URL url = new URL(LOGIN_URL);

                // Create connection object
                HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();

                // Set connection properties
                connection.setRequestMethod("POST");
                connection.setDoOutput(true);
                connection.setRequestProperty("Content-Type", "application/json");

                // Write the payload to the request body
                OutputStream outputStream = connection.getOutputStream();
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream));
                writer.write(payload);
                writer.flush();
                writer.close();
                outputStream.close();

                // Get response from the server
                int responseCode = connection.getResponseCode();

                InputStream inputStream;
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    inputStream = connection.getInputStream();
                } else {
                    inputStream = connection.getErrorStream();
                }

                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line;
                StringBuilder stringBuilder = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    stringBuilder.append(line);
                }
                response = stringBuilder.toString();

                // Close the connections
                reader.close();
                inputStream.close();
                connection.disconnect();

            } catch (IOException e) {
                e.printStackTrace();
            }

            return response;
        }

        @Override
        protected void onPostExecute(String response) {
            super.onPostExecute(response);
            Log.d(TAG, "Response: " + response);

            // Handle the response here
            if (response != null && !response.isEmpty()) {
                try {
                    JSONObject jsonResponse = new JSONObject(response.toString());
                    Log.d(TAG, "step 1");
                    if (jsonResponse.has("token")) {
                        Log.d(TAG, "step 2");
                        String authToken = jsonResponse.getString("token");

                        // HTML encode the authToken before displaying it
                        String encodedAuthToken = Html.escapeHtml(authToken);
                        Log.d(TAG, "authToken: " + authToken);
                        // Save the authentication token securely (e.g., in SharedPreferences)
                        saveAuthToken(encodedAuthToken);


                        // Proceed to the HomeActivity
                        Intent intent = new Intent(MainActivity.this, HomeActivity.class);
                        startActivity(intent);
                        finish(); // Optional: Finish the current activity to prevent going back to it with the back button
                    } else {
                        // Handle error response
                        String errorMessage = jsonResponse.optString("error");
                        // Display the error message to the user
                        // ...
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } else {
                // Handle empty or invalid response
                // Display an error message to the user
                // ...
            }
        }
    }

    private void saveAuthToken(String authToken) {
        // Save the authentication token securely (e.g., in SharedPreferences)
        SharedPreferences preferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
        preferences.edit().putString("auth_token", authToken).apply();
    }
}