package DBConnenct;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.sql.DataSource;

public class DBcon {
	String driver = "org.mariadb.jdbc.Driver";
	String url = "jdbc:mariadb://localhost:3308/data_image";
	Connection conn;
	PreparedStatement pstmt;
	ResultSet rs;
	public DBcon() {
		try {
			Class.forName(driver);
			System.out.println("DB 성공");
			conn = DriverManager.getConnection(url, "root","0431");
			System.out.println("연결 성공");
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	public Connection getCon() {
		return conn;
	}
}
