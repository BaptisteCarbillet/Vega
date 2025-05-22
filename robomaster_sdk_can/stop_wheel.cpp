#include <iostream>

#include <can_streambuf.hpp>
#include <chassis.hpp>


#include <chrono>
#include <thread>

#include <deque>

#include <iomanip>

int main(int, char**)
{
    auto can = can_streambuf("can0", 0x200);
    std::iostream io(&can);
    robomaster::command::chassis chassis(io);
    
    
    chassis.send_workmode(1);
    chassis.send_wheel_speed(0, 0, 0, 0);
    chassis.send_workmode(0);

    

    return 0;
}

