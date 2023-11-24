#include <Wire.h> //INCLUSÃO DA BIBLIOTECA
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#include <WiFi.h>
#include <PubSubClient.h> // Importa a Biblioteca PubSubClient

#define FS300A_PULSE     508         // PULSE / LITRO
#define FS300A_FLOW_RATE 60          // LITRO / MINUTO

#define interruptPin 34

volatile uint16_t pulse;  // Variável que será incrementada na interrupção
float count;           // Variável para armazenar o valor atual de pulse

///
float getVoltas()
{
  if (pulse <= 1)
  {
    Serial.println("Pif" + String(pulse,0));
    return 0;
  }
  Serial.println("P" + String(pulse,0));
  return (((float)pulse/2) - 1) / 3;
}

float frequency;          // Frequência calculada a partir de count
float flowRate;           // Taxa de fluxo calculada a partir da frequência
const float factor = 0.918325;
const float lwf = 0;

portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;  // Mutex para garantir acesso seguro a pulse

// faz o incremento de pulsos, o que eu quero são as voltas
void IRAM_ATTR FlowInterrupt() {
  portENTER_CRITICAL_ISR(&mux);  // Entra em uma seção crítica de interrupção
  ++pulse;  // Incrementa a variável pulse de maneira segura
  portEXIT_CRITICAL_ISR(&mux);   // Sai da seção crítica de interrupção
}

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  
  //lcd.print("Connecting to ");
  //lcd.setCursor(0, 1);
  //lcd.print("WiFi ");
  
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), FlowInterrupt, FALLING);  // Configura a interrupção no pino
}

void loop() {
  
  Frequency();  // Chama a função principal
}

void Frequency() {
  static unsigned long startTime;
  if (micros() - startTime < 1000000UL ) return;   // Intervalo de 1000 milissegundos (1 segundo)
  startTime = micros();

  portENTER_CRITICAL(&mux);  // Entra em uma seção crítica
  count = getVoltas();  // Salva o valor atual de pulse e zera pulse
  pulse = 0;
  portEXIT_CRITICAL(&mux); 

  frequency = count;  // Calcula a frequência
  flowRate = (frequency * factor) - lwf;  // Calcula a taxa de fluxo

  PlotFreq();  // Exibe as informações de Frequencia
  PlotFlux();  // Exibe as informações de Vazão
}

void PlotFreq() {
  lcd.clear();
  lcd.setCursor(0,0);
  Serial.println("Freq.:= " + String(frequency, 2) + " Hz");
  lcd.println("Freq: " + String(frequency, 2) + " Hz");
  //NÃO ME APAGUE: Serial.println(", FLow:= " + String(flowRate, 3) + " L/min");
}

void PlotFlux() {
  lcd.setCursor(0,1);
  Serial.println("Flux.:= " + String(flowRate, 2) + " M^3 * s^-1");
  lcd.println("Flow: " + String(flowRate, 2) + " M^3 * s^-1");
  //NÃO ME APAGUE: Serial.println(", FLow:= " + String(flowRate, 3) + " L/min");
}
