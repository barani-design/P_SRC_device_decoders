uint8_t heater_power = SHT45_I2C_MEAS_T_RH_HIGH_PRECISION;
uint8_t heater_used = 0;

if ( heater_on && ( heater_on <= 3 ) && ( cycles_cnt > 0 ) && ( cycles_cnt <= MAX_HEATER_CYCLES ) )
{
    if ( 1 == heater_on ) heater_power = SHT45_I2C_ACTIVATE_HEATER_20mW_1SEC;
    if ( 2 == heater_on ) heater_power = SHT45_I2C_ACTIVATE_HEATER_110mW_1SEC;
    if ( 3 == heater_on ) heater_power = SHT45_I2C_ACTIVATE_HEATER_200mW_1SEC;
    
    meas_data.heater_on_flag = 1;
    
    for ( int i = 0; i < cycles_cnt; i++ )
    {
        SHT45_clear_new_data_flag( &sht45_data );
        status = SHT45_get_temp_hum_data( &sht45_data, heater_power );
        
        if ( sht45_data.temp_C >= 100.0f )
        {
            debug_printf( LOG_LEVEL_ERROR, CALLER_MEAS, "Temperature too high, stopping heater!\r\n" );
            break;
        }
    }
    heater_used = 1;
}

// Always reset heater flags
heater_on = 0;
cycles_cnt = 0;

// If heater wasn't used (or invalid params), do normal measurement
if ( !heater_used )
{
    status = SHT45_get_temp_hum_data( &sht45_data, SHT45_I2C_MEAS_T_RH_HIGH_PRECISION );
    debug_printf( LOG_LEVEL_DEBUG, CALLER_MEAS, "Normal SHT45 measurement.\r\n" );
}