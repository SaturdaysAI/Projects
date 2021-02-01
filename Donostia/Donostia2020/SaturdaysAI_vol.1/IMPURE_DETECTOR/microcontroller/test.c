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
#include "cmsis_os.h"

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
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim4;

UART_HandleTypeDef huart2;

/* Definitions for TSK_ADC */
osThreadId_t TSK_ADCHandle;
const osThreadAttr_t TSK_ADC_attributes = {
  .name = "TSK_ADC",
  .priority = (osPriority_t) osPriorityNormal,
  .stack_size = 128 * 4
};
/* Definitions for TSK_ACTUATORS */
osThreadId_t TSK_ACTUATORSHandle;
const osThreadAttr_t TSK_ACTUATORS_attributes = {
  .name = "TSK_ACTUATORS",
  .priority = (osPriority_t) osPriorityNormal,
  .stack_size = 128 * 4
};
/* Definitions for TSK_MOTOR */
osThreadId_t TSK_MOTORHandle;
const osThreadAttr_t TSK_MOTOR_attributes = {
  .name = "TSK_MOTOR",
  .priority = (osPriority_t) osPriorityNormal,
  .stack_size = 128 * 4
};
/* USER CODE BEGIN PV */

// GLOBAL VARIABLES
char cad[14];
char buf[4];
char *CMDS[] = {"SEND","ALRM", "ERROR", "DONE"};
uint16_t FLAG = 100;
uint32_t delayance;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_ADC1_Init(void);
static void MX_TIM4_Init(void);
void FTSK_ADC(void *argument);
void FTSK_ACTUATORS(void *argument);
void FTSK_MOTOR(void *argument);

/* USER CODE BEGIN PFP */

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
  MX_USART2_UART_Init();
  MX_ADC1_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */
  __HAL_UART_ENABLE_IT(&huart2, UART_IT_TC); // Habilitación IT_TX
  __HAL_UART_ENABLE_IT(&huart2, UART_IT_RXNE); // // Habilitación IT_RX
  HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3); // Inicialización TIMER4
  /* USER CODE END 2 */

  /* Init scheduler */
  osKernelInitialize();

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of TSK_ADC */
  TSK_ADCHandle = osThreadNew(FTSK_ADC, NULL, &TSK_ADC_attributes);

  /* creation of TSK_ACTUATORS */
  TSK_ACTUATORSHandle = osThreadNew(FTSK_ACTUATORS, NULL, &TSK_ACTUATORS_attributes);

  /* creation of TSK_MOTOR */
  TSK_MOTORHandle = osThreadNew(FTSK_MOTOR, NULL, &TSK_MOTOR_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
  /* add events, ... */
  HAL_UART_Receive_IT(&huart2, buf, 4);

  /* USER CODE END RTOS_EVENTS */

  /* Start scheduler */
  osKernelStart();

  /* We should never get here as control is now taken by the scheduler */
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
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

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 4;
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
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */
  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = ENABLE;
  hadc1.Init.ContinuousConvMode = ENABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 3;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }
  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_112CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_1;
  sConfig.Rank = 2;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_4;
  sConfig.Rank = 3;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM4_Init(void)
{

  /* USER CODE BEGIN TIM4_Init 0 */

  /* USER CODE END TIM4_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM4_Init 1 */

  /* USER CODE END TIM4_Init 1 */
  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 83;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 65535;
  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM4_Init 2 */

  /* USER CODE END TIM4_Init 2 */
  HAL_TIM_MspPostInit(&htim4);

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

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
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, LD2_Pin|ALRM_LED_Pin|BUZZER_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LD2_Pin ALRM_LED_Pin BUZZER_Pin */
  GPIO_InitStruct.Pin = LD2_Pin|ALRM_LED_Pin|BUZZER_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI15_10_IRQn, 5, 0);
  HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);

}

/* USER CODE BEGIN 4 */


void HAL_UART_TxCpltCallback(UART_HandleTypeDef* huart)
{
	HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef* huart)
{
	if(strncmp(buf,CMDS[0],4)==0){       // SEND:msg
		HAL_UART_Transmit_IT(&huart2, cad, sizeof(cad));

	}
	else if(strncmp(buf,CMDS[1],4)==0){  // ALRM:msg

		FLAG = 1;

	}
	else{  // ALRM:msg

		HAL_UART_Transmit_IT(&huart2, CMDS[2], sizeof(CMDS[2]));


	}


	HAL_UART_Receive_IT(&huart2, buf, sizeof(buf));

}

void HAL_GPIO_EXTI_Callback (uint16_t GPIO_Pin)
{
	// SECURITY EVERYTHING READY
	if(HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin) == GPIO_PIN_SET)
	{
			HAL_GPIO_WritePin(ALRM_LED_GPIO_Port, ALRM_LED_Pin, GPIO_PIN_SET);
			HAL_UART_Transmit_IT(&huart2, CMDS[3], sizeof(CMDS[3]));
			FLAG = 0;
			HAL_GPIO_WritePin(ALRM_LED_GPIO_Port, ALRM_LED_Pin, GPIO_PIN_RESET);
		}

}

void SET_PWM(uint16_t valor)
{
	// Configuración PWM
	TIM_OC_InitTypeDef config;
	config.OCMode = TIM_OCMODE_PWM1;
	config.OCPolarity = TIM_OCPOLARITY_HIGH;
	config.OCFastMode =TIM_OCFAST_DISABLE;

	//PWM = 10*valor + 500; // Transformación Grados-> Ticks
	// VALOR:  0-19999
	config.Pulse = valor; // Valor para no hacer la transformación
	HAL_TIM_PWM_ConfigChannel(&htim4, &config, TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3);

}


/* USER CODE END 4 */

/* USER CODE BEGIN Header_FTSK_ADC */
/**
  * @brief  Function implementing the TSK_ADC thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_FTSK_ADC */
void FTSK_ADC(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */

	HAL_StatusTypeDef status;
	float aux;
	uint32_t sens[3];

  for(;;)
  {

		HAL_ADC_Start(&hadc1);

		// TEMP
		status = HAL_ADC_PollForConversion(&hadc1, 1);
		if(status == HAL_OK)
		{
			aux = HAL_ADC_GetValue(&hadc1);
			sens[0] = aux*0.517 -105.1;
		}

		// HUMIDITY
	  status = HAL_ADC_PollForConversion(&hadc1, 1);
	  if(status == HAL_OK){

		  aux = HAL_ADC_GetValue(&hadc1);
		  aux = (aux/ 4095)*1000;
		  sens[1] = aux;
	  }

	  // DISTANCE
	  status = HAL_ADC_PollForConversion(&hadc1, 1);
	  if(status == HAL_OK){
		  aux = HAL_ADC_GetValue(&hadc1);
		  aux = (aux/ 3105)*100 - 2;
		  sens[2] = aux;
	  }

    HAL_ADC_Stop(&hadc1);

    sprintf(cad, "%d,%d,%d;", sens[0],sens[1], sens[2]);
    osDelay(100);


	}

  }
  /* USER CODE END 5 */


/* USER CODE BEGIN Header_FTSK_ACTUATORS */
/**
* @brief Function implementing the TSK_ACTUATORS thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_FTSK_ACTUATORS */
void FTSK_ACTUATORS(void *argument)
{
  /* USER CODE BEGIN FTSK_ACTUATORS */
  /* Infinite loop */
	uint16_t i = 0;
  for(;;)
  {
	  if(FLAG == 1)
	  {
		  delayance = 5000;
		  for(i = 0; i < 20; i++)
		  {
			  HAL_GPIO_TogglePin(BUZZER_GPIO_Port, BUZZER_Pin);
			  HAL_GPIO_TogglePin(ALRM_LED_GPIO_Port, ALRM_LED_Pin);
			  osDelay(200);

		  }
		  HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(ALRM_LED_GPIO_Port, ALRM_LED_Pin, GPIO_PIN_RESET);
		  FLAG = 0;
		  delayance = 0;
	  }

    osDelay(1);
  }
  /* USER CODE END FTSK_ACTUATORS */
}

/* USER CODE BEGIN Header_FTSK_MOTOR */
/**
* @brief Function implementing the TSK_MOTOR thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_FTSK_MOTOR */
void FTSK_MOTOR(void *argument)
{
  /* USER CODE BEGIN FTSK_MOTOR */
  /* Infinite loop */
  uint16_t i;
  for(;;)
  {
	  // 500 - 2500
	  for(i = 500; i <= 2500;i = i+100)
	  {
		  SET_PWM(i);
		  osDelay(5000);
		  osDelay(delayance + 1); // Bug just in case
	  }

    osDelay(1);
  }
  /* USER CODE END FTSK_MOTOR */
}

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
