import { Injectable } from '@nestjs/common';
import { CreateEmployeeDto } from './dto/create-employee.dto';
import { UpdateEmployeeDto } from './dto/update-employee.dto';

@Injectable()
export class EmployeesService {
  private  employees: CreateEmployeeDto[] = [
    {
      id: 1,
      name: `alberto`,
      lastName: `rivera`,
      phoneNumber: `32132131`
    },
    {
      id: 2,
      name: `alan`,
      lastName: `barrera`,
      phoneNumber: `3123123`,
    }
  ]

  create(createEmployeeDto: CreateEmployeeDto) {
    createEmployeeDto.id = this.employees.length+1;//al no tener bd se usa para que no se dupliquen
    //  los id y se agregue este campo en caso de no ponerlo al ingresar un nuevo empleado;
    this.employees.push(createEmployeeDto);
    return CreateEmployeeDto;
  }

  findAll() {
    return this.employees;
  }

  findOne(id: number) {
    const employee = this.employees.filter((employee) => employee.id === id)[0];
    return employee;
  }

  update(id: number, updateEmployeeDto: UpdateEmployeeDto) {
    let employeeToUpdate = this.findOne(id);
    employeeToUpdate = {
      ...employeeToUpdate,
      ...updateEmployeeDto,
    }
    this.employees = this.employees.map((employee)=>{
      if (employee.id === id) {
        employee = employeeToUpdate;
    }
      return employee

    })
    return employeeToUpdate;
  }

  remove(id: number) {
   this.employees = this.employees.filter ((employee)=>employee.id !=id );
   return this.employees;
  }
}
