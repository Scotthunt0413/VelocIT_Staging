
try:
    from ref.sql_tables import create_tables, dynamically_named_tables, name_specs, param_ref, \
        max_star_name_size, float_param, float_param_error, str_param, str_param_error, update_schema_map
except ImportError:
    from mypysql.table_config import create_tables, dynamically_named_tables, name_specs, param_ref, \
        max_star_name_size, float_param, float_param_error, str_param, str_param_error, update_schema_map
