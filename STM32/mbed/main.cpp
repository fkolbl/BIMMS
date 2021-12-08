/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
*   - Add read relays and registers
*   - Handle error
*   - Clean and comment
*/

#include "DigitalOut.h"
#include "PinNames.h"
#include "SPISlave.h"
#include "mbed.h"
#include "nsapi_types.h"
#include "constants.h"


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
SPISlave SPI_AD2(MOSI_AD2,MISO_AD2,SCLK_AD2,SS_AD2);

// Init LED
DigitalOut status_LED(statusLED);
DigitalOut error_LED(errorLED);

// Init Relays
DigitalOut rly1(relay1);
DigitalOut rly2(relay2);
DigitalOut rly3(relay3);
DigitalOut rly4(relay4);
DigitalOut rly5(relay5);
DigitalOut rly6(relay6);
DigitalOut rly7(relay7);
DigitalOut rly8(relay8);
DigitalOut rly9(relay9);
DigitalOut rly10(relay10);
DigitalOut rly11(relay11);
DigitalOut rly12(relay12);
DigitalOut rly13(relay13);
DigitalOut rly14(relay14);
DigitalOut rly15(relay15);
DigitalOut rly16(relay16);
DigitalOut rly17(relay17);
DigitalOut rly18(relay18);
DigitalOut rly19(relay19);
DigitalOut rly20(relay20);
DigitalOut rly21(relay21);
DigitalOut rly22(relay22);
DigitalOut rly23(relay23);

//Tickers 
Ticker ticker_Status_LED;
Ticker ticker_Error_LED;

//global variable 
long int data_from_AD2;
long int data_to_AD2;
short int rxBuff[4];
short int txBuff[4];
short unsigned int spi_idx;
short unsigned int state,new_32bitsSPI; 
long int relay_state ;

int main()
{
    //Init Global Variables
    for (short unsigned int i = 0; i<4; i++)
        {
           rxBuff[i]=0;
           txBuff[i]=0;
        }
    
    data_from_AD2 = 0;
    new_32bitsSPI = 0;
    spi_idx = 0;

    updateRelay(Relay_Default);

    //Init SPI
    SPI_AD2.format(nbits_spi_AD2,spi_mode_AD2);
    SPI_AD2.frequency(spi_freq_AD2);
    SPI_AD2.reply(0);
   
    //Init state 
    state = off_state ;
    InitOffState();

    while (true) {

        if (SPI_AD2.receive()){             //Read SPI register
            TX32bitsSPI();
        }
        if (new_32bitsSPI)
        {
            decode_data(data_from_AD2);
            new_32bitsSPI = 0;
        }
        switch (state)
        {
            case off_state:
                // Do something 
                break;
            case idle_state:
                // Do Something
                break;
            case locked_state:
                // Do Something
                break;
            case error_state: 
                // Do Something 
                break;
        }

    }
}

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
    rly1 = (RelayValue >> 0) & 1UL;
    rly2 = (RelayValue >> 1) & 1UL;
    rly3 = (RelayValue >> 2) & 1UL;
    rly4 = (RelayValue >> 3) & 1UL;
    rly5 = (RelayValue >> 4) & 1UL;
    rly6 = (RelayValue >> 5) & 1UL;
    rly7 = (RelayValue >> 6) & 1UL;
    rly8 = (RelayValue >> 7) & 1UL;
    rly9 = (RelayValue >> 8) & 1UL;
    rly10 = (RelayValue >> 9) & 1UL;
    rly11 = (RelayValue >> 10) & 1UL;
    rly12 = (RelayValue >> 11) & 1UL;
    rly13 = (RelayValue >> 12) & 1UL;
    rly14 = (RelayValue >> 13) & 1UL;
    rly15 = (RelayValue >> 14) & 1UL;
    rly16 = (RelayValue >> 15) & 1UL;
    rly17 = (RelayValue >> 16) & 1UL;
    rly18 = (RelayValue >> 17) & 1UL;
    rly19 = (RelayValue >> 18) & 1UL;
    rly20 = (RelayValue >> 19) & 1UL;
    rly21 = (RelayValue >> 20) & 1UL;
    rly22 = (RelayValue >> 21) & 1UL;
    rly23 = (RelayValue >> 22) & 1UL;
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

void toggleStatusLED()
{
   status_LED=!status_LED; 
}

void toggleErrorLED()
{
   error_LED=!error_LED; 
}

void InitOffState()
{
    ticker_Status_LED.attach(&toggleStatusLED, SLOW_BLINK);
    ticker_Error_LED.detach();
     updateRelay(Relay_Default);
}

void InitIdleState()
{
    ticker_Status_LED.detach();
    ticker_Error_LED.detach();
    status_LED = 1;
    updateRelay(Relay_Default);
}

void InitLockedState()
{
    ticker_Status_LED.attach(&toggleStatusLED, FAST_BLINK);
}

void InitErrorState()
{
    ticker_Status_LED.detach();
    status_LED = 0;
    ticker_Error_LED.attach(&toggleErrorLED, FAST_BLINK);
     updateRelay(Relay_Default);
}


void TX32bitsSPI()
{
    rxBuff[spi_idx] = SPI_AD2.read();
    spi_idx++;
    if (spi_idx==4)
    {
        data_from_AD2 = (rxBuff[0] << 24) | (rxBuff[1] << 16) | (rxBuff[2] << 8) | (rxBuff[3]);
        spi_idx = 0;
        if (data_from_AD2)
            new_32bitsSPI = 1; 
        
    }
    SPI_AD2.reply(txBuff[spi_idx]);
}
   
void Data2buff(long int data)
{
    txBuff[0]=(data >> 24) & 0xFF;
    txBuff[1]=(data >> 16) & 0xFF;
    txBuff[2]=(data >> 8) & 0xFF;
    txBuff[3]=data & 0xFF;
}