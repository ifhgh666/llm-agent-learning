def get_weather(city: str):
    weather_data = {
        "北京": "晴天，25度",
        "上海": "多云，28度",
        "深圳": "小雨，30度"
    }

    return weather_data.get(city, "暂无天气信息")


def get_stock_price(company: str):
    stock_data = {
        "苹果": "190美元",
        "特斯拉": "250美元"
    }

    return stock_data.get(company, "暂无股票信息")


def calculate_bmi(weight: float, height: float):
    bmi = weight / (height ** 2)

    return f"BMI指数是{bmi:.2f}"


def search_recipe(food: str):
    recipes = {
        "鸡蛋": "番茄炒鸡蛋",
        "牛肉": "红烧牛肉"
    }

    return recipes.get(food, "没有找到菜谱")