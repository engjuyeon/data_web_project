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
		String url = "jdbc:mariadb://127.0.0.1:3308/data_image";
		
		String name = "root";
		String password = "0431";
		
		Class.forName(driver);
		Connection con = DriverManager.getConnection(url, name, password);
		String sql = "SELECT * FROM image";
		PreparedStatement pstmt = con.prepareStatement(sql);
		ResultSet rs = pstmt.executeQuery();
		JSONArray arr = new JSONArray();
		
		while(rs.next()){
			JSONObject obj = new JSONObject();
			obj.put("image_id", rs.getString("image_id"));
			obj.put("image", rs.getString("image"));
			
			arr.put(obj);
		}
	
	%>
	<%=arr%>
	