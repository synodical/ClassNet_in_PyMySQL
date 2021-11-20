
import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='', db='university', charset='utf8mb4')

def input_student(sno, sname, grade, dept):
    stud_sql = "insert into student values('" \
               + sno + "', '" + sname + "', " + grade + ", '" + dept + "')"
    try:
        cursor.execute(stud_sql)
        conn.commit()
    except:
        conn.rollback()

def input_course(cno, cname, credit, profname, dept):
    course_sql = "insert into course values('" \
                 + cno + "', '" + cname + "', '" + credit + "', '" + profname + "', '" + dept + "')"
    try:
        cursor.execute(course_sql)
        conn.commit()
    except:
        conn.rollback()

def input_enroll(sno, cno, final, lettergrade):
    enroll_sql = "insert into enroll values('" \
                 + sno + "', '" + cno + "', '" + final + "', '" + lettergrade + "')"
    student_sql = "insert into student values('" + sno + "',NULL,NULL,NULL)"
    course_sql = "insert into course values('" + cno + "',NULL,NULL,NULL,NULL)"
    cursor.execute(student_sql)
    cursor.execute(course_sql)
    cursor.execute(enroll_sql)
    conn.commit()


def select_student(cursor):
    sql = "select * from student"
    cursor.execute(sql)
    print("{0:<7}{1:>22}{2:>10}{3:>19}".format("sno", "sname", "grade", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sno = cur_row[0]
        sname = cur_row[1]
        grade = cur_row[2]
        dept = cur_row[3]
        print("%7s %20s %5s %20s" % (sno, sname, grade, dept))

def select_course(cursor):
    sql = "select * from course"
    cursor.execute(sql)
    print("{0:<4}{1:>33}{2:>9}{3:>20}{4:>20}".format("cno", "cname", "credit", "profname", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        cno = cur_row[0]
        cname = cur_row[1]
        credit = cur_row[2]
        profname = cur_row[3]
        dept = cur_row[4]
        print("%4s %30s %5s %20s %20s" % (cno, cname, credit, profname, dept))

def select_enroll(cursor):
    sql = "select * from enroll"
    cursor.execute(sql)
    print("{0:<7}{1:>4}{2:>8}{3:>20}".format("sno", "cno", "final", "lettergrade"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sno = cur_row[0]
        cno = cur_row[1]
        final = cur_row[2]
        lettergrade = cur_row[3]
        print("%7s %4s %5d %20s" % (sno, cno, final, lettergrade))

cursor = conn.cursor()

# 기존 테이블 삭제
cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS student cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS course cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

sql = "drop table IF EXISTS enroll cascade"
cursor.execute(sql)

# 테이블 생성
sql = "create table student(sno varchar(7), sname varchar(20), grade int, dept varchar(20), primary key (sno))"
cursor.execute(sql)
sql = "create table course(cno varchar(4), cname varchar(30), credit int, profname varchar(20), dept varchar(20), primary key (cno))"
cursor.execute(sql)
sql = """create table enroll(
    sno varchar(7),
    cno varchar(4),
    final int default 0,
    lettergrade varchar(2),
    FOREIGN KEY (sno) REFERENCES student (sno),
    FOREIGN KEY (cno) REFERENCES course (cno),
    PRIMARY KEY (sno, cno)
    )
    """
cursor.execute(sql)

print("0. 종료\n1. student 레코드 검색\n2. course 레코드 검색\n3. enroll 레코드 검색\n4. enroll 레코드 삽입")

input_student('B823019', '홍길동', '4', '컴퓨터')
input_student('B890515', '김철수', '3', '전기')
input_course('C101', '전기회로', '3', '김홍익', '전기')
input_course('C102', '데이터베이스', '4', '이대학', '컴퓨터')

while True:
    cmd = input("기능을 선택하시오 : ")
    if cmd == '0':
        break
    elif cmd == '1':
        select_student(cursor)
    elif cmd == '2':
        select_course(cursor)
    elif cmd == '3':
        select_enroll(cursor)
    else:
        print(">> 4. enroll 레코드 삽입")
        sno = input("학번을 입력하시오: ")
        cno = input("과목번호를 입력하시오: ")
        final = input("기말고사 점수를 입력하시오: ")
        grade = input("학점을 입력하시오: ")
        input_enroll(sno, cno, final, grade)

conn.close()
