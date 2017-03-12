from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN
    import datetime

    start=datetime.datetime(2016,3,1)
    end=datetime.datetime(2017,3,1)
    df=data.DataReader(name="HPQ",data_source="yahoo",start=start,end=end)


    #OR create new column:
    def def_status(open_value,close_value):
        if (open_value <= close_value):
            return "Increase"
        else:
            return "Decrease"

    df["Status"]=[def_status(o,c) for o,c in zip(df.Open,df.Close)]


    df["Middle"]=(df["Open"]+df["Close"])/2
    df["Height"]=abs(df["Close"]-df["Open"])

    p=figure(x_axis_type="datetime",width=1000,height=300,responsive=True)
    p.title.text="Candlestick Chart"
    p.title.text_font_style="normal"
    p.title.align="center"
    p.title.text_font_size='20pt'
    p.grid.grid_line_alpha=0.3


    p.segment(x0=df.index,x1=df.index,y0=df["Low"],y1=df["High"], line_width=1.5, color="black")

    #grey:
    p.rect(x=df.index[df["Status"]=="Increase"], y=df["Middle"][df["Status"]=="Increase"],
           width=43200000,height=df["Height"][df["Status"]=="Increase"],
           fill_color="#E0FFFF", line_color="black")

    #red:
    p.rect(x=df.index[df["Status"]=="Decrease"], y=df["Middle"][df["Status"]=="Decrease"],
           width=43200000,height=df["Height"][df["Status"]=="Decrease"],
           fill_color="#FA8072", line_color="black")


    script1, div1 = components(p)
    cdn_javascript=CDN.js_files[0]
    cdn_css=CDN.css_files[0]

    return render_template("plot.html", script1=script1,
                                        div1=div1,
                                        cdn_css=cdn_css,
                                        cdn_javascript=cdn_javascript)

if __name__ == "__main__":
    app.run(debug=True)
