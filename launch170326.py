#!/usr/bin/python
import RPi.GPIO as gpio
import time
import io
import serial
import picamera

output_file = open('launch-output.txt', 'w')

camera = None
try:
  camera = picamera.PiCamera()
  camera.start_recording("launch-video.h264")
except:
  pass

PROG_START_TIME = int(round(time.time() * 1000.0)) # in milliseconds
PROG_START_MAX_DURATION = 2 # in minutes, can be decimal
PROG_MAX_DURATION = 30 # in minutes, can be decimal
def check_prog_start_time():
  current_time = int(round(time.time() * 1000.0)) # in milliseconds
  elapsed_ms = current_time - PROG_START_TIME
  elapsed_s = elapsed_ms / 1000.0
  elapsed_m = elapsed_s / 60.0
  SERVO_3("==> Total time elapsed: " + str(elapsed_s) + "s")
  if elapsed_m >= PROG_START_MAX_DURATION:
      output_file.write("***Passed maximum program start duration. Quitting.")
      output_file.close()
      try:
        camera.stop_recording()
      except:
        pass
      exit(0)
def check_prog_time():
  current_time = int(round(time.time() * 1000.0)) # in milliseconds
  elapsed_ms = current_time - PROG_START_TIME
  elapsed_s = elapsed_ms / 1000.0
  elapsed_m = elapsed_s / 60.0
  output_file.write("==> Total time elapsed: " + str(elapsed_s) + "s")
  output_file.flush()
  if elapsed_m >= PROG_MAX_DURATION:
      output_file.write("***Passed maximum program duration. Quitting.")
      output_file.close()
      try:
        camera.stop_recording()
      except:
        pass
      exit(0)

SERVO_1 = 2 # servo pin 1
SERVO_2 = 3 # servo pin 2
SERVO_3 = 4 # servo pin 3

EJECTION_CHARGE_PIN = 23
EJECTION_CHARGE_ACTIVATED = 0
EJECTION_CHARGE_DEACTIVATED = 1

SERVO_LOW = [4.5, 5.5, 5.5]
SERVO_HIGH = [6.5, 7.5, 7.4]

PHOTORESISTOR_PIN = 20
PHOTORESISTOR_LIGHT = 0
PHOTORESISTOR_DARK = 1

BUZZER_PIN = 21

SERIAL_DEVICE_NAME = '/dev/ttyUSB0'

LAUNCH_ALT_THRESHOLD = 200 # in feet, on the way up
NUM_LAUNCH_VERIFICATIONS = 30 # number of readings above launch alt before declaring launch
DEPLOY_ALT_THRESHOLD = 750 # in feet, on the way down
NUM_ARM_VERIFICATIONS = 30 # number of readings above deploy alt before 
NUM_DEPLOY_VERIFICATIONS = 30 # number of readings below deploy alt before declaring deployment
NUM_LIGHT_VERIFICATIONS = 5 # number of readings before declaring leg deployment success

LEG_RETRACTION_TIME = 2 # in seconds, can be decimal
LIGHT_WAIT_TIME = 13 # in seconds, can be decimal
LEG_STAGGER_TIME = 3 # in seconds, can be decimal
EJECTION_DURATION = 2 # in seconds, can be decimal

# GPIO setup
gpio.setmode(gpio.BCM)
gpio.setup(EJECTION_CHARGE_PIN, gpio.OUT, initial=EJECTION_CHARGE_DEACTIVATED)
gpio.setup(SERVO_1, gpio.OUT)
gpio.setup(SERVO_2, gpio.OUT)
gpio.setup(SERVO_3, gpio.OUT)
pwm = [gpio.PWM(SERVO_1, 50), gpio.PWM(SERVO_2, 50), gpio.PWM(SERVO_3, 50)]
pwm[0].start(SERVO_HIGH[0])
pwm[1].start(SERVO_HIGH[1])
pwm[2].start(SERVO_HIGH[2])
gpio.setup(PHOTORESISTOR_PIN, gpio.IN)
gpio.setup(BUZZER_PIN, gpio.OUT)

altitudeSerial = None
while True:
    try:
      altitudeSerial = serial.Serial(SERIAL_DEVICE_NAME, baudrate=9600, timeout=2)
      output_file.write("Got serial on " + SERIAL_DEVICE_NAME)
      output_file.flush()
      break
    except:
      check_prog_start_time()
      output_file.write(SERIAL_DEVICE_NAME + " does not exist yet.")
      output_file.flush()

launched = False # whether we're in the air (past launch threshold)
numLaunchVerifications = 0 # number of altitude readings above launch threshold
armed = False # whether we passed deployment altitude
numArmVerifications = 0 # number of altitude readings above deployment threshold

numDeployVerifications = 0 # number of altitude readings below deploy threshold

photoLegSuccessful = False # whether or not we read light on the photoresistor after deploying the first leg
doneDeploying = False # done with all three legs (and ejection if there was light)

def deploy():
        global lightVerifications, photoLegSuccessful, doneDeploying
        ### CHANGEMADE
        ### brunston here: leg deployment changed to 2 -> 3 -> 1
        ### we are changing which leg the photoresistor is physically connected to
        output_file.write("******DEPLOYING******")
        output_file.write(">> Deploying leg 2")
        output_file.flush()
        pwm[1].ChangeDutyCycle(SERVO_LOW[1])
        time.sleep(LEG_RETRACTION_TIME)
        pwm[1].stop()
        output_file.write(">> Deployed leg 2")
        ### ENDCHANGE
        output_file.write(">> Waiting for light...")
        output_file.flush()
        lightMeasureStart = int(round(time.time() * 1000.0)) # in milliseconds
        lightMeasureTime = 0
        lightVerifications = 0 # number of light readings
        while True:
               elapsedMillis = int(round(time.time() * 1000.0)) - lightMeasureStart
               light = gpio.input(PHOTORESISTOR_PIN)
               if light == PHOTORESISTOR_LIGHT:
                       lightVerifications += 1
               else: lightVerifications = 0
               output_file.write("   -- Light " + str(elapsedMillis) + "ms in: " + ("light" if light == PHOTORESISTOR_LIGHT else "dark") + ", # Verifs: " + str(lightVerifications))
               output_file.flush()

               if lightVerifications > NUM_LIGHT_VERIFICATIONS:
                      output_file.write(">> Detected light")
                      output_file.flush()
                      photoLegSuccessful = True
                      lightMeasureTime = elapsedMillis * 1000.0
                      break
               if elapsedMillis > LIGHT_WAIT_TIME * 1000.0:
                      output_file.write(">> Did not detect light, aborting ejection")
                      output_file.flush()
                      photoLegSuccessful = False
                      lightMeasureTime = elapsedMillis * 1000.0
                      break

        # NOTE: EJECTING IS CONNECTED TO LEG 2, AND IS PHYSICALLY SWITCHED BY THE ALTIMETER AND LEG
        # eject if we got light
        #if photoLegSuccessful:
        #    output_file.write(">> Ejecting")
        #    output_file.flush()
        #    gpio.output(EJECTION_CHARGE_PIN, EJECTION_CHARGE_ACTIVATED)
        #    time.sleep(EJECTION_DURATION)
        #    gpio.output(EJECTION_CHARGE_PIN, EJECTION_CHARGE_DEACTIVATED)
        #    output_file.write(">> Done ejecting")
        #    output_file.flush()

        ### CHANGEMADE
        ### BRUNSTON HERE WE ARE CHANGING DEPLOYMENT LEG2 -> LEG3 -> LEG1
        time.sleep(LEG_STAGGER_TIME)
        output_file.write(">> Deploying leg 3")
        output_file.flush()
        pwm[2].ChangeDutyCycle(SERVO_LOW[2])
        time.sleep(LEG_RETRACTION_TIME)
        pwm[2].stop()

        time.sleep(LEG_STAGGER_TIME)
        output_file.write(">> Deploying leg 1")
        output_file.flush()
        pwm[0].ChangeDutyCycle(SERVO_LOW[0])
        time.sleep(LEG_RETRACTION_TIME)
        pwm[0].stop()
        ### ENDCHANGE

        output_file.write(">> Deployment complete!")
        output_file.flush()
        doneDeploying = True
        return

def processAltitude(alt):
        global launched, armed, numLaunchVerifications, numArmVerifications, numDeployVerifications
        if not launched:
            if alt > LAUNCH_ALT_THRESHOLD:
                numLaunchVerifications += 1
            else: numLaunchVerifications = 0

            if numLaunchVerifications > NUM_LAUNCH_VERIFICATIONS:
                launched = True
                output_file.write("******LAUNCHED******")
                output_file.flush()
        elif not armed: # launched, but not armed yet -- below deployment altitude still
            if alt > DEPLOY_ALT_THRESHOLD:
                numArmVerifications += 1
            else: numArmVerifications = 0

            if numArmVerifications > NUM_ARM_VERIFICATIONS:
                armed = True
                output_file.write("******ARMED*******")
                output_file.flush()
        else: # launched and armed, check for deployment
            if alt < DEPLOY_ALT_THRESHOLD:
                numDeployVerifications += 1
            else: numDeployVerifications = 0

            if numDeployVerifications > NUM_DEPLOY_VERIFICATIONS:
                deploy()


# ----START OF EXECUTION----
# try to read altimeter data. run siren until it works
while True:
    if len(altitudeSerial.read(20).encode('ascii')) > 0:
        output_file.write("Read altimeter. Beeping and starting!")
        output_file.flush()
        break

    check_prog_start_time()
    output_file.write("Could not find altimeter reading. Siren!")
    output_file.flush()
    current = 0
    for i in range(1000, 5000):
        current = 1 if current == 0 else 0
        gpio.output(BUZZER_PIN, current)
        time.sleep(1.0/i)
    for i in range(1000, 5000):
        current = 1 if current == 0 else 0
        gpio.output(BUZZER_PIN, current)
        time.sleep(1.0/(6000-i))

# ok, starting launch program. do 4 beeps to indicate start
for _ in range(3):
  for i in range(1000):
      gpio.output(BUZZER_PIN, i % 2)
      time.sleep(1.0/4000.0)
  time.sleep(.75)
for i in range(6000):
    gpio.output(BUZZER_PIN, i % 2)
    time.sleep(1.0/6000.0)

while True:
        alt = None
        data = altitudeSerial.read(20).encode('ascii') # could be lots of lines
        #output_file.write("Data: " + data)
        #output_file.flush()
        if data:
                dataParts = data.split('\n')
                if len(dataParts) > 1:
                        lastData = dataParts[len(dataParts) - 2]

                        gotAlt = False
                        try:
                                alt = int(lastData)
                                gotAlt = True
                        except ValueError:
                                pass
                        if gotAlt and not doneDeploying:
                                processAltitude(alt)
        light = gpio.input(PHOTORESISTOR_PIN)

        if alt == None:
                continue
        altAndLightText = "Alt: " + str(alt) + ", Light: " + ("light" if light == PHOTORESISTOR_LIGHT else "dark")
        if not launched:
            output_file.write("Not Launched >> " + altAndLightText + ", # Launch Verifs: " + str(numLaunchVerifications))
        elif not armed: # launched, not armed yet
            output_file.write("Not armed >> " + altAndLightText + ", # Arm Verifs: " + str(numArmVerifications))
        else: # we launched and armed, and are not in the middle of deploying
            if not doneDeploying:
                output_file.write("Not Deployed >> " + altAndLightText + ", # Deploy Verifs: " + str(numDeployVerifications))
            else:
                output_file.write("Deployed >> " + altAndLightText + ", Successful = " + ("yes" if photoLegSuccessful else "no"))
        output_file.flush()
        check_prog_time()