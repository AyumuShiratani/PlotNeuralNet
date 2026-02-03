
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

def to_mycor():
    return r"""
\def\ResBlockColor{rgb:green,5;red,4;white,5}
\def\AttBlockColor{rgb:red,5;white,5}
\def\InputColor{rgb:yellow,5;green,1;white,5}
"""


# Conv
def to_Res( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" ", opacity=0.7 ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ResBlockColor,
        opacity=""" + str(opacity) + """,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Att( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" ", opacity=0.7 ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\AttBlockColor,
        opacity=""" + str(opacity) + """,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Fc( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" ", opacity=0.7 ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\FcColor,
        opacity=""" + str(opacity) + """,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def Input( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" ", opacity=0.7 ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\InputColor,
        opacity=""" + str(opacity) + """,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""
def block_2Res_sConv(name, botton, top, s_filer, stride, n_filer, offset, size):
    lst = [
        to_Res( name=f'rrc_{name}_r1', s_filer=s_filer, n_filer=n_filer, 
        offset=offset, to=f"({botton}-east)",
        width=size[2], 
        height=size[0], 
        depth=size[1],
        caption=" " ),
        to_Res( name=f'rrc_{name}_r2', s_filer=s_filer, n_filer=n_filer,
         offset="(0,0,0)", to=f'(rrc_{name}_r1-east)',
        width=size[2],
        height=size[0], 
        depth=size[1],
        caption=" " ),
        to_Conv( name=top, s_filer=s_filer//stride if type(s_filer) is int else s_filer , n_filer=n_filer, offset="(0,0,0)", to=f'(rrc_{name}_r2-east)', 
        width=size[2],
        height=size[0]*0.8, 
        depth=size[1]*0.8,    
        caption=" " ),
    to_connection( 
        "{}".format( botton ), 
        f'rrc_{name}_r1'
        )
    ]
    return lst


def block_Unconv_res( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_Res(    name='rr_{}_1'.format(name),       offset="(0,0,0)", to="(unpool_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_Res(    name='{}'.format(top),            offset="(0,0,0)", to="(rr_{}_1-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]

# def to_connection_east_south(of, to, pos=1.25):
#     return rf"""
# \path ({of}-east) -- ({to}-south) coordinate[pos={pos}] ({to}-bottom);
# \draw [connection]
#     ({of}-east)
#     -- node {{\midarrow}} ({to}-bottom)
#     -- ({to}-south);
# """

# def to_connection_east_south(of, to):
#     return rf"""
# \draw [connection]
#     ({of}-east) -| node {{\midarrow}} ({to}-south);
# """


def to_connection_east_south(of, to):
    return rf"""
\coordinate ({to}-below) at ({to}-south |- {of}-east);
\draw [connection]
    ({of}-east)
    -- ({to}-below)
    -- node {{\midarrow}} ({to}-south);
"""


def to_image(pathfile,
             to='(-3,0,0)',
             width=8,
             height=8,
             name="temp",
             xshift=0):
    return rf"""
\node[
    canvas is zy plane at x={xshift}
] ({name}) at {to}
{{\includegraphics[width={width}cm,height={height}cm]{{{pathfile}}}}};
"""

def chg_font():
    return "\normalsize"


arch = [ 
    to_head('..'), 
    to_cor(),
    to_mycor(),
    to_begin(),
    chg_font(),
    #input
    to_input( 'input.jpg' , name="Input_image"),


    #block-001
    # to_ConvConvRelu( name='ccr_b1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40  ),
    to_Res( name='rrc_b1_r1', s_filer="", n_filer="", offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ),
    to_Res( name='rrc_b1_r2', s_filer="", n_filer="", offset="(0,0,0)", to="(rrc_b1_r1-east)", width=1, height=40, depth=40, caption=" " ),
    to_Conv( name='rrc_b1_c', s_filer="", n_filer="", offset="(0,0,0)", to="(rrc_b1_r2-east)", width=1, height=40*0.8, depth=40*0.8, caption=" " ),
    # to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b2-east)", width=1, height=32, depth=32, opacity=0.5),
    
    *block_2Res_sConv( name='b2', botton='rrc_b1_c', top='rrc_b2_c', s_filer="", stride=2, n_filer="", offset="(1.5,0,0)", size=(30,30,2.5)), # size=(32,32,2.5)
    *block_2Res_sConv( name='b3', botton='rrc_b2_c', top='rrc_b3_c', s_filer="", stride=2, n_filer="", offset="(1.5,0,0)", size=(24,24,3.5)), # size=(25.6,25.6,3.5)
    *block_2Res_sConv( name='b4', botton='rrc_b3_c', top='rrc_b4_c', s_filer="", stride=2, n_filer="", offset="(1.5,0,0)", size=(20.5,20.5,4.5)),
    *block_2Res_sConv( name='b5', botton='rrc_b4_c', top='rrc_b5_c', s_filer="", stride=2, n_filer="", offset="(1.5,0,0)", size=(16.3,16.3,4.5)),
    *block_2Res_sConv( name='b6', botton='rrc_b5_c', top='rrc_b6_c', s_filer="", stride=2, n_filer="", offset="(1.5,0,0)", size=(13.1,13.1,4.5)),
    #Bottleneck
    #block-005
    # to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(rrc_b6_c-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    # to_connection( "rrc_b6_c", "ccr_b5"),

    to_Res( name='b7_r1', s_filer="", n_filer="", offset="(1.5,0,0)", to="(rrc_b6_c-east)", width=4.5, height=8, depth=8, caption=" " ),
    to_Att( name='b7_a', s_filer="", n_filer="", offset="(0,0,0)", to="(b7_r1-east)", width=4.5, height=8, depth=8, caption=" " ),
    to_Res( name='b7_r2', s_filer="", n_filer="", offset="(0,0,0)", to="(b7_a-east)", width=4.5, height=8, depth=8, caption=" " ),
    to_connection( "rrc_b6_c", "b7_r1"),
    #Decoder
    # *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    *block_Unconv_res(name="b8", botton="b7_r2", top='end_b8', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(13.1,13.1,4.5), opacity=0.5),
    to_skip( of='rrc_b6_r2', to='rr_b8_1', pos=1.25),
    # *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    *block_Unconv_res(name="b9", botton="end_b8", top='end_b9', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(16.3,16.3,4.5), opacity=0.5),
    to_skip( of='rrc_b5_r2', to='rr_b9_1', pos=1.25),    

    *block_Unconv_res(name="b10", botton="end_b9", top='end_b10', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(20.5,20.5,4.5), opacity=0.5),
    to_skip( of='rrc_b4_r2', to='rr_b10_1', pos=1.25),    

    *block_Unconv_res(name="b11", botton="end_b10", top='end_b11', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(25.6,25.6,3.5), opacity=0.5),
    to_skip( of='rrc_b3_r2', to='rr_b11_1', pos=1.25),    

    *block_Unconv_res(name="b12", botton="end_b11", top='end_b12', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(32,32,2.5), opacity=0.5),
    to_skip( of='rrc_b2_r2', to='rr_b12_1', pos=1.25),    


    *block_Unconv_res(name="b13", botton="end_b12", top='end_b13', s_filer="",  n_filer="", offset="(1.6,0,0)", size=(40,40,1), opacity=0.5),
    to_skip( of='rrc_b1_r2', to='rr_b13_1', pos=1.25),    

    to_Conv( name='final', s_filer="", n_filer="", offset="(3.1,0,0)", to="(end_b13-east)", width=1, height=40, depth=40, caption=" " ),
    to_connection( "end_b13", "final"),
    #input
    to_image( 'random.jpg' , name="Output_image", to="(final-east)", xshift=1.0),
    # *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    # to_skip( of='rrc_b2_r2', to='ccr_res_b8', pos=1.25),    
    
    # *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    # to_skip( of='rrc_b1_r2', to='ccr_res_b9', pos=1.25),
    
    # to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="SOFT" ),
    # to_connection( "end_b9", "soft1"),
     
    # to_input( '../examples/fcn8s/cats.jpg' , name="time input", to="(0,0,25)"),
    Input(name="timeinput", s_filer="", n_filer="", offset="(0,0,0)", to="(0,0,15)", height=1, depth=1, width=1 ,caption="Time Step"),
    to_Fc(name="time_embetting", s_filer="", n_filer="", offset="(1.5,0,0)", to="(timeinput-east)", height=1, depth=16, width=1 ),
    to_connection( "timeinput", "time_embetting"),
    to_connection_east_south( "time_embetting", "rrc_b1_r1"),
    to_connection_east_south( "time_embetting", "rrc_b2_r1"),
    to_connection_east_south( "time_embetting", "rrc_b3_r1"),
    to_connection_east_south( "time_embetting", "rrc_b4_r1"),
    to_connection_east_south( "time_embetting", "rrc_b5_r1"),
    to_connection_east_south( "time_embetting", "rrc_b6_r1"),
    to_connection_east_south( "time_embetting", "b7_r1"),
    to_connection_east_south( "time_embetting", "b7_r2"),
    to_connection_east_south( "time_embetting", "rr_b8_1"),
    to_connection_east_south( "time_embetting", "rr_b9_1"),
    to_connection_east_south( "time_embetting", "rr_b10_1"),
    to_connection_east_south( "time_embetting", "rr_b11_1"),
    to_connection_east_south( "time_embetting", "rr_b12_1"),
    to_connection_east_south( "time_embetting", "rr_b13_1"),

    to_Res( name='sample_res', s_filer="", n_filer="", offset="(20,0,20)", to="(0,0,0)", width=4, height=4, depth=4, caption="ResBlock" ),
    to_Conv( name='sample_conv', s_filer="", n_filer="", offset="(3,0,0)", to="(sample_res-east)", width=4, height=4, depth=4, caption="Convolution" ),
    to_Att( name='sample_att', s_filer="", n_filer="", offset="(3,0,0)", to="(sample_conv-east)", width=4, height=4, depth=4, caption="Attention Block" ),
    to_UnPool( name='sample_unpool', offset="(3,0,0)", to="(sample_att-east)", width=4, height=4, depth=4, caption="Transposed convolution" ),
    to_Fc( name='sample_embedding', s_filer="", n_filer="", offset="(3,0,0)", to="(sample_unpool-east)", width=4, height=4, depth=4, caption="Time embedding Block" ),
    to_end() 
    ]

arch2 = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(pool1-east)", height=32, depth=32, width=2 ),
    to_connection( "pool1", "conv2"),
    to_Pool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    to_SoftMax("soft1", 10 ,"(3,0,0)", "(pool1-east)", caption="SOFT"  ),
    to_connection("pool2", "soft1"),
    to_end()
    ]
def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
