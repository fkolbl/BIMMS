/* 
 * Constant file for BIMMS measurement device - STM32 Code
 * 	Authors: Florian Kolbl / Louis Regnacq
 *	(c) ETIS - University Cergy-Pontoise
 *		IMS - University of Bordeaux
 *		CNRS
 */

#ifndef CONSTANTS_H
#define CONSTANTS_H

// Unique Identification Number 
#define DEVICE_ID         0x01

// SPI AD2 Settings
#define MISO_AD2          PA_6          
#define MOSI_AD2          PA_7
#define SCLK_AD2          PA_5
#define SS_AD2            PA_4
#define nbits_spi_AD2     8            // 8 bits transaction 
#define spi_mode_AD2      3            // SPI mode
#define spi_freq_AD2      1000000      // SPI CLK

#define Relay_Default     0b00000000000000000000000

//STM32 Globlal State
#define off_state       0
#define idle_state      1
#define locked_state    2
#define error_state     3

//Command 
#define set_state  0x01
#define set_relays 0x02
#define read_reg   0x03

//Mask for incomming data 
#define Mask_data 0x00FFFFFFF
#define shift_com 29

//LEDs
#define statusLED   PC_1
#define errorLED    PC_0
#define SLOW_BLINK  1s
#define FAST_BLINK  100ms

//SWITCHES
#define SW1         PC_2
#define SW2         PC_3

//Relays
#define relay1      PB_0
#define relay2      PB_1
#define relay3      PB_2
#define relay4      PB_3
#define relay5      PB_4
#define relay6      PB_5
#define relay7      PB_6
#define relay8      PB_7
#define relay9      PB_8
#define relay10     PB_9
#define relay11     PB_10
#define relay12     PB_11
#define relay13     PB_12
#define relay14     PB_13
#define relay15     PB_14
#define relay16     PB_15
#define relay17     PC_9
#define relay18     PC_10
#define relay19     PC_11
#define relay20     PC_12
#define relay21     PC_13
#define relay22     PC_14
#define relay23     PC_15

//Register Address map for reading
#define ID_add          0
#define state_add       1
#define error_add       2
#define relays_map_add  3



#endif 