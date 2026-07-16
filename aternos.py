import asyncio
import os
from playwright.async_api import async_playwright
from config import ATERNOS_USER, ATERNOS_PASSWORD


SESSION_FILE = "sessions/aternos_state.json"


async def get_browser():

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=True
    )

    context = await browser.new_context(
        storage_state=SESSION_FILE if os.path.exists(SESSION_FILE) else None
    )

    page = await context.new_page()

    return playwright, browser, context, page



async def login(page, context):

    await page.goto(
        "https://aternos.org/go/"
    )

    await asyncio.sleep(3)

    # Si ya está logueado
    if "dashboard" in page.url:
        return True


    # Login
    await page.fill(
        'input[name="user"]',
        ATERNOS_USER
    )

    await page.fill(
        'input[name="password"]',
        ATERNOS_PASSWORD
    )

    await page.click(
        "button[type=submit]"
    )


    await page.wait_for_timeout(5000)


    await context.storage_state(
        path=SESSION_FILE
    )


    return "dashboard" in page.url



async def start_server():

    playwright, browser, context, page = await get_browser()

    try:

        if not await login(page, context):
            return "❌ No se pudo iniciar sesión en Aternos"


        await page.goto(
            "https://aternos.org/server/"
        )


        await page.wait_for_timeout(3000)


        start_button = page.locator(
            "button#start"
        )


        if await start_button.is_visible():

            await start_button.click()

            await page.wait_for_timeout(5000)

            return "▶️ Servidor iniciándose..."

        return "⚠️ El servidor ya está iniciado o no encontré el botón"


    except Exception as e:

        return f"❌ Error: {e}"


    finally:

        await browser.close()
        await playwright.stop()



async def stop_server():

    playwright, browser, context, page = await get_browser()

    try:

        if not await login(page, context):
            return "❌ No se pudo iniciar sesión"


        await page.goto(
            "https://aternos.org/server/"
        )


        await page.wait_for_timeout(3000)


        stop_button = page.locator(
            "button#stop"
        )


        if await stop_button.is_visible():

            await stop_button.click()

            return "⏹️ Servidor apagándose"


        return "⚠️ No encontré el botón de apagar"


    except Exception as e:

        return f"❌ Error: {e}"


    finally:

        await browser.close()
        await playwright.stop()