from bot.core.get_vars import get_val
from bot.core.handlers.settings_copy_menu import handle_settings_copy_menu
from bot.core.set_vars import set_val
from bot.uploaders.rclone_transfer import rclone_copy_transfer
import logging
from bot.utils.get_rclone_conf import get_config

torlog = logging.getLogger(__name__)



async def handle_setting_copy_menu_callback(callback_query):
    conf_path = await get_config()
    data = callback_query.data.decode()
    cmd = data.split("^")
    mmes = await callback_query.get_message()

    if callback_query.data == "pages":
        await callback_query.answer()

    #1 --- rclone_menu_copy    

    if cmd[1] == "list_drive_origin":
        set_val("ORIGIN_DRIVE", cmd[2])
        origin_drive= get_val("ORIGIN_DRIVE")
        set_val("ORIGIN_DIR", "/")
        await handle_settings_copy_menu(
            query= callback_query, 
            mmes= mmes, 
            edit=True,
            msg= f'Seleccione directorio origen\n\nRuta: `{origin_drive}`', 
            drive_name= cmd[2],
            submenu="list_drive", 
            is_dest_drive=False, 
            data_cb="list_dir_origin",
            is_second_menu=False
           )

    elif cmd[1] == "list_dir_origin":
        origin_drive = get_val("ORIGIN_DRIVE")
        origin_dir= get_val("ORIGIN_DIR")
        rclone_dir= origin_dir + cmd[2] +"/"
        set_val("ORIGIN_DIR", rclone_dir)
        await handle_settings_copy_menu(
             callback_query,
             mmes, 
             edit=True, 
             msg=f"Seleccione carpeta para subir\n\nRuta:`{origin_drive}:{rclone_dir}`", 
             drive_base=origin_dir, 
             drive_name= origin_drive,
             rclone_dir= cmd[2], 
             data_cb="list_dir_origin",
             submenu="list_drive",
             is_second_menu= False
             )

    elif cmd[1] == "rclone_menu_copy":
        origin_dir= get_val("ORIGIN_DIR")
        rclone_dir= origin_dir + cmd[2] +"/"
        set_val("ORIGIN_DIR", rclone_dir)
        await handle_settings_copy_menu(
             callback_query,
             mmes, 
             edit=True, 
             msg=f"Seleccione unidad destino", 
             submenu="rclone_menu_copy", 
             data_cb="list_drive_dest"
             )                         
  
    elif cmd[1] == "list_drive_dest":
        set_val("DEST_DRIVE", cmd[2])
        dest_drive= get_val("DEST_DRIVE")
        await handle_settings_copy_menu(
            callback_query, 
            mmes, edit=True, 
            msg=f'Seleccione directorio destino\n\nRuta: `{dest_drive}`', 
            drive_name= cmd[2],
            submenu="list_drive", 
            data_cb="list_dir_dest",
            is_second_menu=True
            )

    elif cmd[1] == "list_dir_dest":
        dest_drive = get_val("DEST_DRIVE")
        dest_dir= get_val("DEST_DIR")
        rclone_dir= dest_dir + cmd[2] +"/"
        set_val("DEST_DIR", rclone_dir)
        await handle_settings_copy_menu(
             callback_query,
             mmes, 
             edit=True, 
             msg=f"Seleccione carpeta para subir\n\nRuta:`{dest_drive}:{rclone_dir}`", 
             drive_base=dest_dir, 
             drive_name= dest_drive,
             data_cb="list_dir_dest",
             rclone_dir= cmd[2], 
             submenu="list_drive", 
             is_second_menu= True
             )        
 
    elif cmd[1] == "start_copy":
        await rclone_copy_transfer(callback_query, conf_path)                               

    # close menu
    elif cmd[1] == "selfdest":
        await callback_query.answer("Closed")
        await callback_query.delete()