/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#define DEVICE_ID         0x09

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

#define SLOW_BLINK  1s
#define FAST_BLINK  100ms

//Register Address map for reading
#define ID_add          0
#define state_add       1
#define error_add       2
#define relays_map_add  3

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define relay21_Pin GPIO_PIN_13
#define relay21_GPIO_Port GPIOC
#define relay22_Pin GPIO_PIN_14
#define relay22_GPIO_Port GPIOC
#define relay23_Pin GPIO_PIN_15
#define relay23_GPIO_Port GPIOC
#define errorLED_Pin GPIO_PIN_0
#define errorLED_GPIO_Port GPIOC
#define statusLED_Pin GPIO_PIN_1
#define statusLED_GPIO_Port GPIOC
#define SW1_Pin GPIO_PIN_2
#define SW1_GPIO_Port GPIOC
#define SW2_Pin GPIO_PIN_3
#define SW2_GPIO_Port GPIOC
#define SS_Pin GPIO_PIN_4
#define SS_GPIO_Port GPIOA
#define SS_EXTI_IRQn EXTI4_IRQn
#define relay1_Pin GPIO_PIN_0
#define relay1_GPIO_Port GPIOB
#define relay2_Pin GPIO_PIN_1
#define relay2_GPIO_Port GPIOB
#define relay3_Pin GPIO_PIN_2
#define relay3_GPIO_Port GPIOB
#define relay11_Pin GPIO_PIN_10
#define relay11_GPIO_Port GPIOB
#define relay12_Pin GPIO_PIN_11
#define relay12_GPIO_Port GPIOB
#define relay13_Pin GPIO_PIN_12
#define relay13_GPIO_Port GPIOB
#define relay14_Pin GPIO_PIN_13
#define relay14_GPIO_Port GPIOB
#define relay15_Pin GPIO_PIN_14
#define relay15_GPIO_Port GPIOB
#define relay16_Pin GPIO_PIN_15
#define relay16_GPIO_Port GPIOB
#define relay17_Pin GPIO_PIN_9
#define relay17_GPIO_Port GPIOC
#define relay18_Pin GPIO_PIN_10
#define relay18_GPIO_Port GPIOC
#define relay19_Pin GPIO_PIN_11
#define relay19_GPIO_Port GPIOC
#define relay20_Pin GPIO_PIN_12
#define relay20_GPIO_Port GPIOC
#define relay4_Pin GPIO_PIN_3
#define relay4_GPIO_Port GPIOB
#define relay5_Pin GPIO_PIN_4
#define relay5_GPIO_Port GPIOB
#define relay6_Pin GPIO_PIN_5
#define relay6_GPIO_Port GPIOB
#define relay7_Pin GPIO_PIN_6
#define relay7_GPIO_Port GPIOB
#define relay8_Pin GPIO_PIN_7
#define relay8_GPIO_Port GPIOB
#define relay9_Pin GPIO_PIN_8
#define relay9_GPIO_Port GPIOB
#define relay10_Pin GPIO_PIN_9
#define relay10_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
