package com.example.myapplication;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class HomeActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static final String API_URL = "https://rise-and-reflect.onrender.com/display_tasks/";
    private static final String PREFS_NAME = "MyPrefs";
    private static final String AUTH_TOKEN_KEY = "auth_token";

    private TextView usernameTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        usernameTextView = findViewById(R.id.usernameTextView);

        SharedPreferences sharedPreferences = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        String authToken = sharedPreferences.getString(AUTH_TOKEN_KEY, "");
        Log.e(TAG, "authToken" + authToken);

        if (!authToken.isEmpty()) {
            // If authentication token exists, send it to the server for verification
            new AuthTask().execute(authToken);
        } else {
            // Handle case when authentication token is not found
            Log.e(TAG, "Authentication token not found in SharedPreferences");
        }
    }

    private class AuthTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String authToken = params[0];
            String result = "";

            try {
                URL url = new URL(API_URL);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setDoOutput(true);

                JSONObject jsonParam = new JSONObject();
                jsonParam.put("auth_token", authToken);

                OutputStream outputStream = connection.getOutputStream();
                outputStream.write(jsonParam.toString().getBytes("UTF-8"));
                outputStream.flush();
                outputStream.close();

                int responseCode = connection.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String line;

                    while ((line = reader.readLine()) != null) {
                        response.append(line);
                    }

                    reader.close();
                    result = response.toString();
                } else {
                    Log.e(TAG, "HTTP error code: " + responseCode);
                }

                connection.disconnect();
            } catch (Exception e) {
                Log.e(TAG, "Exception: " + e.getMessage());
            }

            return result;
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            Log.d(TAG, "result: " + result);

            try {
                JSONObject jsonResponse = new JSONObject(result.toString());
                Log.d(TAG, "jsonResponse: " + jsonResponse);
                String username = jsonResponse.getString("username");
                Log.d(TAG, "username: " + username);
                usernameTextView.setText(username);
            } catch (JSONException e) {
                Log.e(TAG, "JSON parsing error: " + e.getMessage());
            }
        }
    }
}
