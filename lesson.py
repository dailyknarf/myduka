class Student:
   def __init__(self,name,student_no,course):
      self.name = name
      self.student_no = student_no
      self.course = course

   def study(self,unit):
      print(f"{self.name} studies {unit}")

   def play(self,game):
      print(f"{self.name} plays {game}")

   def sleep(self,time):
      print(f"{self.name} sleeps {time}")

   def get_details(self):
      print("user details")
      print(f"Name:{self.name}, Student_no:{self.student_no}, Course:{self.course}")
      print("_______________________________")
      
#object 1
student1 = Student("Paul","11","computer science")
print(type(student1))

student1.study("computer ssience")
student1.play("football")
student1.sleep("11pm")
student1. get_details()

#object2
student2 = Student("Frank","12","data science")
print(type(student2))

student2.study("data science")
student2.play("tennis")
student2.sleep ("10pm")
student2. get_details()