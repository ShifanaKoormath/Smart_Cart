#include "HX711.h"

#define DT 2
#define SCK 3

HX711 scale;

float calibration_factor = -98.64;

float last_stable_weight = 0;
float current_weight = 0;

float delta_threshold = 5;       // ignore noise below 5g
int stabilization_delay = 1200;  // wait for weight stabilization

void setup() {

  Serial.begin(9600);

  scale.begin(DT, SCK);
  scale.set_scale(calibration_factor);
  scale.tare();

  Serial.println("Smart Cart Weight Sensor Ready");

  delay(2000);

  last_stable_weight = scale.get_units(10);
}

void loop() {

  current_weight = scale.get_units(5);

  float delta = current_weight - last_stable_weight;

  // Ignore small noise
  if (abs(delta) < delta_threshold) {
    delay(200);
    return;
  }

  // Wait for stabilization
  delay(stabilization_delay);

  float stabilized_weight = scale.get_units(10);
  float final_delta = stabilized_weight - last_stable_weight;

  if (abs(final_delta) < delta_threshold) {
    return;
  }

  int rounded_delta = round(final_delta);

  if (rounded_delta > 0) {

    Serial.print("ADD:");
    Serial.println(rounded_delta);

  } else {

    Serial.print("REMOVE:");
    Serial.println(abs(rounded_delta));

  }

  last_stable_weight = stabilized_weight;

  delay(800);
}