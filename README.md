# GeneralAPI
### GeneralAPI is an all purpose REST API that returns JSON data for many categories from generating QR codes and crypto exchange rates to random dad jokes.
# Endpoints:
## Generating QR code
### GET "https://general-api.vercel.app/qr/generate?data="
### Response example:
```
{
"QR_URL":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcwAAAHMAQAAAABwoKUrAAABVklEQVR42u3dQW7DIBAFUNQLcP9b+gapFKUxMOBKkRhn8VhYwuFtWHyNxyQpj0/HUVAURTfSo4zjee+9YrXkp3w8UBRF/xltDsUwOqdxiR1GUXR7Nh0hql7TdV7ZYRRFs7PpfIirsglF0W/KptlFNqEomptNsd80n+o3oSial03LWsp7OhRF78qmxWhbTdPjB3YYRdGMbAph9KyW6vvT8pqqm1AUTXumq20YnZfhXtcQt8Moim6um86Uuj7p1K2zwyiKpmVTWzeVUEZ1x53sMIqim7OpbTCVy+NOD/0mFEWzs2k4wTS8tvsro9RNKIpmZNOxyqvl4fDqDAGKohnZNC+ZhtZ4V0HJJhRFM7Jp9nauzi+e6VAUvSubroondROKorfWTSV0o7rOkx1GUXR7NsV+U/t1ldr/1Jzv06EompJN4V48UhCbTnYYRdGd2eQvH1AU/Tr6C2lfsq92YuBDAAAAAElFTkSuQmCC
}
```
### Optional parameters:
• back_color: str <br>
• front_color: str<br>
• scale: int<br>
• border_size: int<br>
• border_color: str<br>
