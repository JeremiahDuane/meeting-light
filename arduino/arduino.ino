#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include "config.h" 

#define RED_LED 13
#define BLUE_LED 14
#define GREEN_LED 12
bool running = false;

void RED() {
  digitalWrite(RED_LED, HIGH); 
}
void BLUE() {
  digitalWrite(BLUE_LED, HIGH); 
}
void ORANGE() {
  digitalWrite(RED_LED, HIGH); 
  analogWrite(GREEN_LED, 64);
}
void GREEN() {
  digitalWrite(GREEN_LED, HIGH); 
}
void OFF() {
  digitalWrite(RED_LED, LOW); 
  digitalWrite(BLUE_LED, LOW); 
  digitalWrite(GREEN_LED, LOW);
}

; // 
WiFiServer server(wifi_port);
 
void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_pswd);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available() && client.available() != 0){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request
  if (request.indexOf("/RED") > 0)  {
    OFF();
    RED();
  }
  if (request.indexOf("/ORANGE") >0)  {
    OFF();
    ORANGE();
  }
  if (request.indexOf("/GREEN") > 0)  {
    OFF();
    GREEN();
  }
  if (request.indexOf("/OFF") > 0)  {
    OFF();
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("");
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("Led pin is set");
  client.println("</html>");
 }