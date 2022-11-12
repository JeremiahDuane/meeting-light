#include <EEPROM.h>
#include <ESP8266WiFi.h>
#define RED_LED 12
#define WHITE_LED 13
#define GREEN_LED 14

void RED() {
  digitalWrite(RED_LED, HIGH); 
}
void WHITE() {
  digitalWrite(WHITE_LED, HIGH); 
}
void GREEN() {
  digitalWrite(GREEN_LED, HIGH); 
}
void OFF() {
  digitalWrite(RED_LED, LOW); 
  digitalWrite(WHITE_LED, LOW); 
  digitalWrite(GREEN_LED, LOW);
}
const char* ssid = "jgage_netgear";
const char* password = "melodicboat789";

; // 
WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(RED_LED, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
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
  if (request.indexOf("/WHITE") >0)  {
    OFF();
    WHITE();
  }
  if (request.indexOf("/GREEN") > 0)  {
    OFF();
    GREEN();
  }
  if (request.indexOf("/OFF") > 0)  {
    OFF();
  }
}