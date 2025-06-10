import logging
import os
from dotenv import load_dotenv
import qrcode
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN in environment variables.")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DIGIPIN_GRID = [
    ['F', 'C', '9', '8'],
    ['J', '3', '2', '7'],
    ['K', '4', '5', '6'],
    ['L', 'M', 'P', 'T']
]

BOUNDS = {
    'minLat': 2.5,
    'maxLat': 38.5,
    'minLon': 63.5,
    'maxLon': 99.5
}

def encode_digipin(lat, lon):
    if lat < BOUNDS['minLat'] or lat > BOUNDS['maxLat']:
        raise ValueError('Latitude out of range')
    if lon < BOUNDS['minLon'] or lon > BOUNDS['maxLon']:
        raise ValueError('Longitude out of range')

    min_lat, max_lat = BOUNDS['minLat'], BOUNDS['maxLat']
    min_lon, max_lon = BOUNDS['minLon'], BOUNDS['maxLon']
    digipin = ''

    for level in range(1, 11):
        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        row = 3 - int((lat - min_lat) / lat_div)
        col = int((lon - min_lon) / lon_div)

        row = max(0, min(row, 3))
        col = max(0, min(col, 3))

        digipin += DIGIPIN_GRID[row][col]

        if level in [3, 6]:
            digipin += '-'

        max_lat = min_lat + lat_div * (4 - row)
        min_lat = min_lat + lat_div * (3 - row)
        min_lon = min_lon + lon_div * col
        max_lon = min_lon + lon_div

    return digipin

def decode_digipin(digipin):
    pin = digipin.replace('-', '')
    if len(pin) != 10:
        raise ValueError('Invalid DIGIPIN length')

    min_lat, max_lat = BOUNDS['minLat'], BOUNDS['maxLat']
    min_lon, max_lon = BOUNDS['minLon'], BOUNDS['maxLon']

    for char in pin:
        found = False
        for r in range(4):
            for c in range(4):
                if DIGIPIN_GRID[r][c] == char:
                    row, col = r, c
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f'Invalid DIGIPIN character: {char}')

        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        lat1 = max_lat - lat_div * (row + 1)
        lat2 = max_lat - lat_div * row
        lon1 = min_lon + lon_div * col
        lon2 = min_lon + lon_div * (col + 1)

        min_lat, max_lat = lat1, lat2
        min_lon, max_lon = lon1, lon2

    return round((min_lat + max_lat) / 2, 6), round((min_lon + max_lon) / 2, 6)

def generate_qr_code(digipin):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(digipin)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


# /start or /help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📍 *DIGIPIN Bot Help*\n"
        "Available commands:\n"
        "`/encode <lat> <lon>` - Encode to DIGIPIN\n"
        "`/decode <digipin>` - Decode to lat/lon\n"
        "📍 Or share your location directly to encode it"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

# /encode command
async def encode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 2:
            raise ValueError("Usage: /encode <lat> <lon>")
        lat = float(context.args[0])
        lon = float(context.args[1])
        pin = encode_digipin(lat, lon)
        await update.message.reply_text(f'📦 DIGIPIN: `{pin}`', parse_mode='Markdown')
        qr_image = generate_qr_code(pin)
        qr_image_path = 'digipin_qr.png'
        qr_image.save(qr_image_path)
        with open(qr_image_path, 'rb') as qr_file:
            await update.message.reply_photo(photo=qr_file, caption='📷 QR Code for DIGIPIN')
        os.remove(qr_image_path)  # Clean up the QR code image file
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {e}')

# /decode command
async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 1:
            raise ValueError("Usage: /decode <digipin>")
        digipin = context.args[0]
        lat, lon = decode_digipin(digipin)
        google_maps_url = f'https://www.google.com/maps/search/?api=1&query={lat},{lon}'
        await update.message.reply_text(f'🌍 Latitude: `{lat}`\n🌐 Longitude: `{lon}`', parse_mode='Markdown')
        await update.message.reply_text(f'🔗 Google Maps: {google_maps_url}')
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {e}')

# Handle shared location
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        location = update.message.location
        lat = location.latitude
        lon = location.longitude
        pin = encode_digipin(lat, lon)
        await update.message.reply_text(f'📍 Location DIGIPIN: `{pin}`', parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f'❌ Error encoding location: {e}')

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("encode", encode))
    app.add_handler(CommandHandler("decode", decode))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("Bot is running...")
    app.run_polling()
