/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

TIM_HandleTypeDef htim2;

/* USER CODE BEGIN PV */
long int data_from_AD2;
long int data_to_AD2;
uint8_t rxBuff[4];
uint8_t txBuff[4];
short unsigned int state,new_32bitsSPI;
long int relay_state ;


int cnt_fast;
int cnt_slow;
uint8_t tick_slow;
uint8_t tick_fast;
int div_cnt_fast;
int div_cnt_slow;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
static void MX_TIM2_Init(void);
/* USER CODE BEGIN PFP */

void decode_data(long int data_from_AD2);
void update_state(long int data);
void send_register(long int add);

void updateRelay(long int RelayValue);

void toggleStatusLED();
void toggleErrorLED();

void InitOffState();
void InitIdleState();
void InitLockedState();
void InitErrorState();

void TX32bitsSPI();
void Data2buff(long int data);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */




  //Init Global Variables
  for (short unsigned int i = 0; i<4; i++)
      {
         rxBuff[i]=0;
         txBuff[i]=0;
      }

  data_from_AD2 = 0;
  new_32bitsSPI = 0;


   cnt_fast = 0;
   cnt_slow = 0;
   tick_slow = 0;
   tick_fast = 0;
   div_cnt_fast = 10;
   div_cnt_slow = 80;

   HAL_GPIO_WritePin(statusLED_GPIO_Port, statusLED_Pin,0);
   HAL_GPIO_WritePin(errorLED_GPIO_Port, errorLED_Pin,0);

  updateRelay(Relay_Default);

  //Init state
  state = off_state ;
  InitOffState();

  HAL_TIM_Base_Start_IT(&htim2);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

      if (new_32bitsSPI)
      {
          decode_data(data_from_AD2);
          new_32bitsSPI = 0;
      }
      switch (state)
      {
          case off_state:
        	  if (tick_slow)
        	  {
        		  tick_slow = 0;
        		  HAL_GPIO_TogglePin(statusLED_GPIO_Port, statusLED_Pin);
        	  }
        	  // Do Something
              break;
          case idle_state:
              // Do Something
              break;
          case locked_state:
        	  if (tick_fast)
        	  {
        		  tick_fast = 0;
        		  HAL_GPIO_TogglePin(statusLED_GPIO_Port, statusLED_Pin);
        	  }
              // Do Something
              break;
          case error_state:
        	  if (tick_fast)
        	  {
        		  tick_fast = 0;
        		  HAL_GPIO_TogglePin(errorLED_GPIO_Port, errorLED_Pin);
        	  }
              // Do Something
              break;
      }






    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV2;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_SLAVE;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_HIGH;
  hspi1.Init.CLKPhase = SPI_PHASE_2EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_64;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 100;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 7200;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, relay21_Pin|relay22_Pin|relay23_Pin|errorLED_Pin
                          |statusLED_Pin|relay17_Pin|relay18_Pin|relay19_Pin
                          |relay20_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, relay1_Pin|relay2_Pin|relay3_Pin|relay11_Pin
                          |relay12_Pin|relay13_Pin|relay14_Pin|relay15_Pin
                          |relay16_Pin|relay4_Pin|relay5_Pin|relay6_Pin
                          |relay7_Pin|relay8_Pin|relay9_Pin|relay10_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : relay21_Pin relay22_Pin relay23_Pin errorLED_Pin
                           statusLED_Pin relay17_Pin relay18_Pin relay19_Pin
                           relay20_Pin */
  GPIO_InitStruct.Pin = relay21_Pin|relay22_Pin|relay23_Pin|errorLED_Pin
                          |statusLED_Pin|relay17_Pin|relay18_Pin|relay19_Pin
                          |relay20_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : SW1_Pin SW2_Pin */
  GPIO_InitStruct.Pin = SW1_Pin|SW2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : SS_Pin */
  GPIO_InitStruct.Pin = SS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(SS_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : relay1_Pin relay2_Pin relay3_Pin relay11_Pin
                           relay12_Pin relay13_Pin relay14_Pin relay15_Pin
                           relay16_Pin relay4_Pin relay5_Pin relay6_Pin
                           relay7_Pin relay8_Pin relay9_Pin relay10_Pin */
  GPIO_InitStruct.Pin = relay1_Pin|relay2_Pin|relay3_Pin|relay11_Pin
                          |relay12_Pin|relay13_Pin|relay14_Pin|relay15_Pin
                          |relay16_Pin|relay4_Pin|relay5_Pin|relay6_Pin
                          |relay7_Pin|relay8_Pin|relay9_Pin|relay10_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI4_IRQn, 10, 0);
  HAL_NVIC_EnableIRQ(EXTI4_IRQn);

}

/* USER CODE BEGIN 4 */
void decode_data(long int data)
{
    short int command = (data >> shift_com) & 0xFF ;
    switch (command)
    {
        case set_state:
            update_state(data & Mask_data);
            break;

        case read_reg:
            send_register(data & Mask_data);
            break;

        case set_relays:
            if (state == idle_state)
            {
                updateRelay (data & Mask_data);
            }
    }
}

void update_state(long int data)
{
    switch (data)
    {
        case off_state:
            state = off_state;
            InitOffState();
            break;
        case idle_state:
            state = idle_state;
            InitIdleState();
            break;
        case locked_state:
            state = locked_state;
            InitLockedState();
            break;
        default:
            state = error_state;
            InitErrorState();
            break;

    }
}

void updateRelay(long int RelayValue)
{
    relay_state=RelayValue;
    HAL_GPIO_WritePin(relay1_GPIO_Port, relay1_Pin,(RelayValue >> 0) & 1UL);
    HAL_GPIO_WritePin(relay2_GPIO_Port, relay2_Pin,(RelayValue >> 1) & 1UL);
    HAL_GPIO_WritePin(relay3_GPIO_Port, relay3_Pin,(RelayValue >> 2) & 1UL);
    HAL_GPIO_WritePin(relay4_GPIO_Port, relay4_Pin,(RelayValue >> 3) & 1UL);
    HAL_GPIO_WritePin(relay5_GPIO_Port, relay5_Pin,(RelayValue >> 4) & 1UL);
    HAL_GPIO_WritePin(relay6_GPIO_Port, relay6_Pin,(RelayValue >> 5) & 1UL);
    HAL_GPIO_WritePin(relay7_GPIO_Port, relay7_Pin,(RelayValue >> 6) & 1UL);
    HAL_GPIO_WritePin(relay8_GPIO_Port, relay8_Pin,(RelayValue >> 7) & 1UL);
    HAL_GPIO_WritePin(relay9_GPIO_Port, relay9_Pin,(RelayValue >> 8) & 1UL);
    HAL_GPIO_WritePin(relay10_GPIO_Port, relay10_Pin,(RelayValue >> 9) & 1UL);
    HAL_GPIO_WritePin(relay11_GPIO_Port, relay11_Pin,(RelayValue >> 10) & 1UL);
    HAL_GPIO_WritePin(relay12_GPIO_Port, relay12_Pin,(RelayValue >> 11) & 1UL);
    HAL_GPIO_WritePin(relay13_GPIO_Port, relay13_Pin,(RelayValue >> 12) & 1UL);
    HAL_GPIO_WritePin(relay14_GPIO_Port, relay14_Pin,(RelayValue >> 13) & 1UL);
    HAL_GPIO_WritePin(relay15_GPIO_Port, relay15_Pin,(RelayValue >> 14) & 1UL);
    HAL_GPIO_WritePin(relay16_GPIO_Port, relay16_Pin,(RelayValue >> 15) & 1UL);
    HAL_GPIO_WritePin(relay17_GPIO_Port, relay17_Pin,(RelayValue >> 16) & 1UL);
    HAL_GPIO_WritePin(relay18_GPIO_Port, relay18_Pin,(RelayValue >> 17) & 1UL);
    HAL_GPIO_WritePin(relay19_GPIO_Port, relay19_Pin,(RelayValue >> 18) & 1UL);
    HAL_GPIO_WritePin(relay20_GPIO_Port, relay20_Pin,(RelayValue >> 19) & 1UL);
    HAL_GPIO_WritePin(relay21_GPIO_Port, relay21_Pin,(RelayValue >> 20) & 1UL);
    HAL_GPIO_WritePin(relay22_GPIO_Port, relay22_Pin,(RelayValue >> 21) & 1UL);
    HAL_GPIO_WritePin(relay23_GPIO_Port, relay23_Pin,(RelayValue >> 22) & 1UL);

}

void send_register(long int add)
{
   switch (add)
    {
        case ID_add:
            Data2buff((long int)DEVICE_ID);
            break;
        case state_add:
           Data2buff((long int)state);
            break;

        default :
            Data2buff((long int)0x00);
            break;
    }
}


void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef* htim)
{

	if (htim->Instance == TIM2)
	{

		 if (cnt_slow >= div_cnt_slow)
		  {
			  cnt_slow = 0 ;
			  tick_slow = 1;

		  }
		  else
		  {
			  cnt_slow++;
		  }

		 if (cnt_fast >= div_cnt_fast)
		  {
			 cnt_fast = 0 ;
			 tick_fast = 1;

		  }
		  else
		  {
			  cnt_fast++;
		  }
	}
}


void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if(GPIO_Pin == SS_Pin)
    {
    	HAL_SPI_TransmitReceive(&hspi1, txBuff,rxBuff, 4, 10);
        data_from_AD2 = (rxBuff[0] << 24) | (rxBuff[1] << 16) | (rxBuff[2] << 8) | (rxBuff[3]);

        HAL_SPI_DeInit(&hspi1); // reset the state machine back to original state
        HAL_SPI_Init(&hspi1) ;	//avoid false detection (dirty hack but ...)

        if (data_from_AD2)
            new_32bitsSPI = 1;
    }
}


void Data2buff(long int data)
{
    txBuff[0]=(data >> 24) & 0xFF;
    txBuff[1]=(data >> 16) & 0xFF;
    txBuff[2]=(data >> 8) & 0xFF;
    txBuff[3]=data & 0xFF;
}

void InitOffState()
{
    updateRelay(Relay_Default);
    HAL_GPIO_WritePin(errorLED_GPIO_Port, errorLED_Pin,0);
}

void InitIdleState()
{

    updateRelay(Relay_Default);
	HAL_GPIO_WritePin(statusLED_GPIO_Port, statusLED_Pin,1);
}

void InitLockedState()
{
	//Do something
}

void InitErrorState()
{
	HAL_GPIO_WritePin(statusLED_GPIO_Port, statusLED_Pin,0);
    updateRelay(Relay_Default);
}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
