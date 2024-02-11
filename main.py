from database import Academy,Student
import sys
if __name__=='__main__':
    
    name=input("Enter your name : ")
    
    print("Select the Academy :")
    academies=Academy.get_all_academy()
    for academy in academies:
        print (f"{academy.id} {academy.name} {academy.course} {academy.fee} ")
        
    academy_choice = int(input("Enter your Choice  "))
    
    is_already_enroll=Student.check_enrollement_status(name,academy_choice)
    if is_already_enroll==True:
        print("You are already enrolled ! ")
        new_enrollement=input(" Do you want to join the Academy Again !! yes or no")
        if new_enrollement=='no':
            sys.exit()
    
    new_student=Student.add_student(name,academy_choice,fee_paid=0)
    selected_academy=next(filter(lambda x:x.id==academy_choice,academies))

    
    print("Enter your choice!")
    print("[1] Start the Session ")
    print("[2] Dropout")
    choice=int(input())
    if choice==2:
        new_student.drop_out()
        print("You have been dropout !")
        sys.exit()
    
    if choice==1:
        print(f"Total fee is: {selected_academy.fee}")
        fee=input("Enter the amount you want to pay: ")
        new_student=new_student.pay_fee(fee)
        new_student=new_student.clear_first_session()
        print("First session has been cleared ")
        
        
        
    
    print("Enter your choice!")
    print("[1] Start next  the Session ")
    print("[2] Dropout")
    choice=int(input())
    if choice==2:
        new_student.drop_out()
        print("You have been dropout !")
        sys.exit()
    
    if choice==1:
        remaining_fee=selected_academy.fee-new_student.fee_paid
        if remaining_fee <0:
            print("You have paid more fee .Please contact office")
        if remaining_fee ==0:
            new_student.clear_second_session()
            print("Second session cleared ")
        if remaining_fee>0:
            print(f"remaining fee is {remaining_fee}")
            while True:
                fee=int(input("Please enter the remaining fee:"))
                if fee!=remaining_fee:
                    print("Amount do not match . Please enter again !")
                else:
                    break
        new_student=new_student.pay_fee(new_student.fee_paid + fee)
        new_student=new_student.clear_second_session()
        print("Second session has been cleared !")
        