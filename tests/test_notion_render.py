from math2notion.notion_render import NotionRender
from mistletoe import Document
from notion_client import Client
import pypandoc

from tests import notion_token, page_id

tex_text = r"""
\section{相关函数}

相关函数Correlation Function也称自相关函数Auto Correlation Function,是一个二元函数,对于随机过程$X(t)$,其相关函数为：
\begin{equation}
    R_X(t, s) = E(X(t) X(s))
\end{equation}

我们依旧可以把相关函数看作某种内积,因此不难得到相关函数的下面特点：

\begin{itemize}
    \item 对称性：$R_X(t, s)=R_X(s, t)$
    \item 非负性：$R_X(t, t)=E(X(t) X(t)) \leq 0$
    \item 柯西不等式：$|R_X(t, s)| \leq (R_X(s, s)R_X(t, t)) ^ \frac{1}{2}$
\end{itemize}

我们令$X = (X(t_i),\cdots,X(t_n))^\top$,可以定义\textbf{相关矩阵}Correlation Matrix：

\begin{equation}
    \begin{aligned}
        R_X =& (R_X(t_i, t_j))_{ij}\\
        =& (E[X(t_i)X(t_j)])_{ij}\\
        =& E[XX^\top]
    \end{aligned}
\end{equation}
"""


def test_upload():
    render = NotionRender()
    md_text = pypandoc.convert_text(tex_text, "md", "tex")
    doc = Document(md_text)
    render.upload(doc, notion_token, page_id)


def test_render():
    render = NotionRender()
    md_text = pypandoc.convert_text(tex_text, "md", "tex")

    doc = Document(md_text)
    block_list = render.render(doc)
