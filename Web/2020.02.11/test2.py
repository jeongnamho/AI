html = """
<html>
   <head>
      <meta charset="utf-8">
   </head>

   <body>
      <font color=cyan> @out</font>

      <table border=1>
         <tr>
            <td> 이름 </td> <td> <font color=Plum> @name </font> </td>
         </tr>
         <tr>
            <td> email </td> <td> @email </td>
         </tr>
      </table>
   </body>
</html>
"""

html = html.replace("@out",  "제목출력")
html = html.replace("@name",  "정남호")
html = html.replace("@email",  "jnh7807@gmail.com")

print(html)