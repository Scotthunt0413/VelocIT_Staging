max_star_name_size = 50
max_param_type_len = 20
max_len_str_param = 100
max_ref_len = 50
max_units_len = 10
max_notes_len = 100

max_spectral_handle_len = 100
max_output_filename_len = 200

# how the website updates the tables
update_schema_map = [('example_db', 'new_example_db')]

name_specs = F"VARCHAR({max_star_name_size}) NOT NULL, "
param_name = F"VARCHAR({max_param_type_len}) NOT NULL, "
float_spec = f"FLOAT"
float_param = f"{float_spec} NOT NULL, "
float_param_error = f"{float_spec}, "
str_param = F"VARCHAR({max_len_str_param}) NOT NULL, "
str_param_error = F"VARCHAR({max_len_str_param}), "
param_ref = F"VARCHAR({max_ref_len}), "
param_units = F"VARCHAR({max_units_len}), "
param_notes = F"VARCHAR({max_notes_len}), "



create_tables = {"object_params_float": "CREATE TABLE `object_params_float` "
                                                   "(`float_index_params` int(11) NOT NULL AUTO_INCREMENT," +
                                                    "`spexodisks_handle` " + name_specs +
                                                    "`float_param_type` " + param_name +
                                                    "`float_value` " + str_param +
                                                    "`float_error_low` " + str_param_error +
                                                    "`float_error_high` " + str_param_error +
                                                    "`float_ref` " + param_ref +
                                                    "`float_units` " + param_units +
                                                    "`float_notes` " + param_notes +
                                                    "PRIMARY KEY (`float_index_params`)" +
                                                    ") " +
                                                   "ENGINE=InnoDB;"}

dynamically_named_tables = {"spectrum": "(`wavelength_um` " + float_param +
                            "`flux` " + float_param_error +
                            "`flux_error` " + float_param_error +
                            "PRIMARY KEY (`wavelength_um`)" +
                            ") ENGINE=InnoDB;"}
