spanish_text = {
    "welcome_message": "Bienvenido a @Profit Crypto Bot",
    "tutorial_name": "KuCoin API Keys [Tutorial] por ShrimpyApp",
    "folder_warning": "CUIDADO: NO MODIFICAR ESTA CARPETA",
    "log_in_menu": {
        "yes": "s",
        "no": "n",
        "options": ["Crear Usuario", "Seleccionar Usuario", "Borrar Usuario"],
        "select_titles": [
            "Seleccionar opcion",
            "Seleccionar usuario",
            "Borrar usuario",
        ],
        "create_user": {
            "form_name": "Forma de creacion de usuario.",
            "success_message": "Usuario {} Creado Satisfactoriamente!",
            "username": "Introducir Nombre de Usuario: ",
            "already_exists_error": "Usuario {} ya existe.",
            "invalid_username_error": "Usuario Invalido {}",
            "api_queries": [
                "Introducir API Kucoin: ",
                "Intruducir API secret: ",
                "Introducir Kucoin API passphrase: ",
            ],
            "invalid_api_error": "Informacion API de Kucoin invalida:",
        },
        "fetch_user_success": "Usuario {} seleccionado satisfactoriamente!",
        "confirm_delete": "Estas seguro de que quieres borrar el usuario {}?",
        "delete_success": "Usuario {} borrado",
    },
    "run_task": {
        "yes": "s",
        "n": "n",
        "confirm": "¿Confirmar?",
        "confirm_task": "Tarea en funcionamiento {} con la siguiente configuración",
        "starting_task": "Arrancar Tarea: ",
        "info": (
            "Pulsa CTRL+C en cualquier momento para cancelar la tarea en funcionamiento.\n"
            "Si cancela es posible que algunos trades queden abiertos en Kucoin.\n"
        ),
        "insufficient_balance": "Balance insuficiente para arrancar el bot.\nañade balance en tu cuenta de Kucoin para continuar.",
        "task_menu": {
            "options": [
                "Crear Tarea",
                "Seleccionar Tarea",
                "Ver Tareas",
                "Borrar Tarea",
            ],
            "select_titles": [
                "Seleccionar opcion",
                "Arrancar tarea",
                "Ver tareas",
                "Borrar tareas",
            ],
            "create_task": {
                "form_name": "Forma de creacion de tareas.",
                "info": [
                    "El tamaño de la orden es la cantidad en {} que será utilizada para cada compra.",
                    "Maximo de compra es el maximo numero de ordenes de compra sin completar la venta.",
                    "El porcentaje de compra es el porcentaje de bajada desde el precio de referencia para abrir una orden de compra.",
                    "El porcentaje de venta es el porcentaje de subida desde el precio de referencia para abrir una orden de venta.",
                    "Si decides mantener tus ganancias invertidas, tu ganancia se reflejara en {}.",
                ],
                "inputs": [
                    "Tamaño de la orden",
                    "Maximo de compra",
                    "Porcentaje de compra",
                    "Porcentaje de venta",
                ],
                "task_name": "Nombre de la nueva tarea: ",
                "confirm_profits": "Mantener ganancias invertidas? ",
                "yes": "s",
                "no": "n",
                "success_message": "Task {} Creada Satisfactoriamente",
                "invalid_task": "Nombre de la tarea Invalido: {}",
                "task_exists": "Task {} Ya existe",
                "input_field": "Input {}: ",
                "input_set_message": "{} Seleccionado a: {} {}",
                "invalid_input_message": "Entrada Invalida por {}: {}",
            },
            "copy_task": {
                "info": "Reproducing task {}",
                "success_message": "New task {} Creada Satisfactoriamente",
                "task_name": "Nombre de la nueva tarea: ",
                "invalid_task": "Tarea para copiar invalida: {}",
                "task_exists": "Tarea {} Ya existe",
            },
            "view_task": {
                "header": "Tarea {} Configuracion",
                "task_config_not_found": "No se pudo ver la configuracion de la tarea por que no se encotro",
                "task_trades_not_found": "No se pudo ver la configuracion de los trades por que no se encontro",
                "bot_config": {
                    "trade_size": "Tamaño de la orden",
                    "buy_percent": "Porcentaje de compra",
                    "sell_percent": "Porcentaje de venta",
                    "max_trades": "Maximo de compra",
                    "keep_profits_invested": "Mantener Ganancias Invertidas",
                },
                "task_trades": {
                    "trades_title": "Trades completadas",
                    "trades_columns": [
                        "KuCoin Order ID",
                        "Side",
                        "Date",
                        "Time",
                        "Precio (ETH/USDT)",
                        "Cantidad (en ETH)",
                        "Fee (en USDT)",
                    ],
                },
                "profits": "Ganancias por los ciclos completados: {} {}",
            },
            "delete_task": {
                "confirm": "¿Seguro que quieres borrar esta tarea {}?",
                "yes": "s",
                "no": "n",
                "task_deleted": "Tarea {} borrada.",
            },
        },
        "user_interrupted": "EL USUARIO INTERRUMPIO LA TAREA",
        "rate_limited": "Has sido limitado por exceso de solicitudes. Por favor espera 6 minutos...",
        "market_info": {
            "market_price": "Precio de mercado",
            "target_price": "Precio marcado como objetivo",
            "balance": "Balance",
            "stop_buy": "Maximo numero de compras alcanzado",
            "requests": "Solicitudes Kucoin",
            "time_elapsed": "Tiempo transcurrido",
            "buy": "comprar",
            "sell": "vender",
            "completed_cycles": "Ciclos Completados",
        },
        "yes": "s",
        "no": "n",
    },
}
