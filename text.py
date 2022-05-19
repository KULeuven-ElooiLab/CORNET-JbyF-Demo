import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
from st_clickable_images import clickable_images
import base64

def centerImage(pathImage,width,underscript):
    images = []
    
    with open(pathImage, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    clicked = clickable_images(
                images,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={'width':f'{width}'},
            )
    if underscript!='':
        st.markdown(f"<p style='text-align: center; color: grey;'>{underscript}</p>", unsafe_allow_html=True)
    return clicked

def render_latex(formula, fontsize=12, dpi=600 ):
    """Renders LaTeX formula into Streamlit."""
    fig = plt.figure()
    text = fig.text(0, 0, '$%s$' % formula, fontsize=fontsize)
    
    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) +0.05
    # set the size of the fig equal to that of the textbox
    fig.set_size_inches((6.15,height))

    # adjusting the postion of the fig so it is in the middle of the textbox
    dy = (bbox.ymin / float(dpi)) / height
    dx = (1-(width / 6.15))/2 # in percentages
    text.set_position((dx, -dy))

    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, format='jpg')
    plt.close(fig)
    
    st.image(buffer)


def intro():

    st.markdown("""
    # Description of the project
    Currently the design of mechanical joining processes like self-pierce riveting with 
    semi-tubular rivet (SPR-ST) and clinching for production is subject to complex and experimental test 
    series in which process parameters such as the rivet or die geometry are varied iteratively and based 
    on experience until a suitable joint contour and strength is achieved. To simplify the use of mechanical 
    joining technologies, these development cycles and thereby the effort for implementation into production must be reduced.
    """)

    centerImage(pathImage='docs/IntroPic.png',width='70%',
            underscript='Basic parameters that can be measured during a cross section analysis')
    

    st.markdown("### Data-based algorithms")
    

    
    st.markdown("""
    ### Analytical formulas
    To predict the strength using analytical formulas, a literature review was done. Papers were found only for 
    clinch joints. When predicting the strength with analytical formulas, it is important to know that there are two dominant 
    failure mechanisms. The first dominant failure mode is fracture in the punch side sheet. The second failure mode is 
    completely dominated by plastic deformation. In this case, the clinch joint will locally deform hereby reducing the 
    interlock between both sheets eventually leading to unbuttoning of the joint. In practice, a combination of both failure modes occurs.
    The predominant failure mode of the clinch is determined by the calculated lower bound strength.
    """)

def analytical_General():
    st.write('''
    ### General
    Based on several parameters is it possible to predict the force of the joint. These calculations are divided into 2 groups of failure. 
    Viz, deformation and fracture dominant failure. In the literature, various equations have been found for both the pull-out and the shear 
    tensile tests. Based on 50 cases, we defined the best performing equations. 
    ''')

    centerImage(pathImage='docs/Analytical.jpg',width='80%',
            underscript='')

    st.write('''
    Those 4 equations are used in this web application. 
    To know the strength of the joint in a particular loading condition, you need to calculated the strength of both failure modes. 
    The lowest calculated strength will be the strength of the joint in that condition. 
    ''')

def analytical_howItWorks():
    st.write('''
    ### How it works
    On the left, you have the sidebar with all parameters needed for the calculations. 
    You can fill those in for one particular case. Or, in case you want to predict the strength 
    of multiple joints at once, there is also a tool where you upload your excel file with all the data. 
    You can download the template in the sidebar and re-upload it with your data.
    \n In order to understand the parameters, a small description can be found below. 
    Also, the discription of the formulas:
    ''')

def analytical_TT():
    

    st.write('''
    #### Top tensile test
    The deformation process during a top tensile test can be compared with that of the **tube sinking process without a mandrel**. This implies 
    that the die-side sheet can be seen as a rigid ‘die’. The most basic formula applies when the clinch is simplified to a tube. Because of 
    oversimplification, the maximum force will be underestimated. According to Coppieters et al. [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg), 
    the bottom part of the clinch contributes to the strength as it is radially compressed when assuming a rigid die (original). If the edges of the shape are more strictly delineated, 
    by means of the typical geometric parameters, an even better prediction of the force is obtained.
    > *The maximum top tensile force of **deformation-dominant failure** is calculated according to Coppieters (see below). But with different boundary conditions.*
    ''')

    
    
    render_latex(r"F_{def} = {A_n\left[-\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A^{Rod}_{entry}}\right)^{\beta}\right]}{A^{Tube}_{entry}}+\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)\right)\left(\frac{A^{Tube}_{entry}}{A_n}\right)^{\frac{\omega}{2\pi}}\right]}")

    # render_latex(r"F_{def} = {A_{n,tube}\left[\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A_f}\right)^{\beta}\right]}{A^{Tube}_{entry}}-\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)\right)\left(\frac{A_{n,tube}}{A^{Tube}_{entry}}\right)^{\beta}\right]}")
    st.write('''
    The top sheet is the thinnest in the neck region meaning that the joint will fracture in this region. This failure mode can be compared to an 
    uniaxial tensile test on a tubular specimen with a thickness equal to the neck thickness [[2]](https://www.sciencedirect.com/science/article/pii/S0261306909006220). This calculation is fully analytical when the area is derived from experimental data.
    > *The **fracture strength** can be calculated as follows:*
    ''')
    render_latex(r'''F_{frac} = A_n\sigma_{UTS}''')
    
def analytical_ST():
    st.write('''
    #### Shear lap tensile test
    When applying a shear load on two clinched sheets, a complex deformation of the joint and sheets will occur. The most simplified 
    representation is a tube under shear loading. Due to the large deformation and associated strain hardening of the sheets during clinching, the local yield stress has increased.
    Therefore, numerical data is needed to determine the yield stress after joining (AFS)''')
    render_latex(r'''F_{def} = A_n\frac{\sigma_{AFS}}{\sqrt{3}}''')
    st.write('''
    An empirical method was used to calculate the strength until fracture. 
    ''')
    render_latex(r'''F_{frac} = \frac{t_1\alpha}{4}(2d+\alpha t_1)\pi\sigma_{UTS} \quad with: \quad \alpha=0.4''')
    
def results(strengthTT,modeTT,strengthST,modeST):
    st.write(f'''
    Based on the manual input, we expect the joint to fail around **{strengthTT} during a top tensile test**. Where {modeTT} failure is dominant. 
    During **a shear lap test**, we predict that the joint can withstand **{strengthST}** with {modeST} as dominant failure mode.
    \n The results of all 4 calculations can be seen in the table below: 
    ''')

def  Machine_General():
    st.write('''
    ### General
     
    ''')

    centerImage(pathImage='docs/ML1.jpg',width='65%',
            underscript='')

    
    