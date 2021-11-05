    <%@ page import="java.sql.ResultSet" %>
    <%@ page import="java.sql.PreparedStatement" %>
    <%@ page import="java.sql.Connection" %>
    <%@ page import="java.sql.SQLException" %>
    <%@ page import="java.sql.DriverManager" %>
    <%@ page import="org.json.JSONObject" %>
    <%@ page import="org.json.JSONArray" %>
    <%@ page language="java" contentType="application/json; charset=UTF-8"
    pageEncoding="UTF-8"%>

	<%
		String driver = "org.mariadb.jdbc.Driver";
		String url = "jdbc:mariadb://127.0.0.1:3308/public_data_analysis";
		
		String name = "root";
		String password = "0431";
		
		Class.forName(driver);
		Connection con = DriverManager.getConnection(url, name, password);
		String sql = "SELECT P.기간, P.계, AP.total, E.total, G.gdp, O.합계, B.출생건수, B.사망건수, U.total FROM seoul_population AS P LEFT JOIN economically_active_population AS AP ON P.기간 = AP.year LEFT JOIN employment_rate AS E ON AP.year = E.year LEFT JOIN gdp AS G ON E.year = G.year LEFT JOIN one_person AS O ON G.year = O.기간 LEFT JOIN seoul_birth_death AS B ON O.기간 = B.기간 LEFT JOIN unemployment_rate AS U ON B.기간 = U.year ORDER BY P.기간";
		PreparedStatement pstmt = con.prepareStatement(sql);
		ResultSet rs = pstmt.executeQuery();
		JSONArray arr = new JSONArray();
		
		while(rs.next()){
			JSONObject obj = new JSONObject();
			obj.put("year", rs.getString("P.기간"));
			obj.put("population", rs.getString("P.계"));
			obj.put("activity_population", rs.getString("AP.total"));
			obj.put("employment_rate", rs.getString("E.total"));
			obj.put("gdp", rs.getString("G.gdp"));
			obj.put("one_person", rs.getString("O.합계"));
			obj.put("birth", rs.getString("B.출생건수"));
			obj.put("death", rs.getString("B.사망건수"));
			obj.put("unemployment_rate", rs.getString("U.total"));
			
			arr.put(obj);
		}
	
	%>
	<%=arr%>
	