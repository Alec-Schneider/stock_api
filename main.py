from typing import Union
from equity import Equity
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response, FileResponse
import matplotlib.pyplot as plt
from io import BytesIO 
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stocks/{ticker}")
def read_item(ticker: str, start_date: str, end_date: str):
    e = Equity()
    data = e.download_ticker(ticker, start_date, end_date)
    data = e.track_50_200_signal(data)
    # Convert DataFrame to JSON table
    json_table = data.reset_index().to_json(orient="table", index=False)

    # Return the JSON table as the response
    # return JSONResponse(content=json_table)

    # Save the plot to a BytesIO object
    fig, ax = plt.subplots(1)
    data[['50_day_ma', '200_day_ma']].plot(ax=ax, title=ticker)
    data[data["cross50"] == 1].reset_index().plot(kind="scatter", x="Date", y="cross_price", ax=ax, c="green", marker="^")
    data[data["cross50"] == -1].reset_index().plot(kind="scatter", x="Date", y="cross_price", ax=ax, c="red", marker="v")

    plot_buffer = BytesIO()
    fig.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)

    return Response(content=plot_buffer.getvalue(), media_type="image/png")
    
    #  both of these fail
    # return Response(content=json_table, media_type="application/json"), Response(content=plot_buffer.getvalue(), media_type="image/png")
    # return Response(content=json_table, media_type="application/json"), FileResponse(plot_buffer.getvalue(), media_type="image/png")
