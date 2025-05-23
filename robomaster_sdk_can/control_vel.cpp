#include <iostream>

#include <can_streambuf.hpp>
#include <chassis.hpp>


#include <chrono>
#include <thread>

#include <deque>

#include <iomanip>

int main(int argc, char* argv[])
{
    auto can = can_streambuf("can0", 0x200);
    std::iostream io(&can);
    robomaster::command::chassis chassis(io);


    std::vector<int16_t> wheel_speed;
    for (int i = 1; i < argc; ++i)
    {
        std::string s = argv[i];
        wheel_speed.push_back(std::stoi(s));
    }
    int16_t fr_rpm = wheel_speed[0];
    int16_t fl_rpm = wheel_speed[1];
    int16_t bl_rpm = wheel_speed[2];
    int16_t br_rpm = wheel_speed[3];  

    chassis.send_workmode(1);

    chassis.send_wheel_speed(fr_rpm, fl_rpm, bl_rpm, br_rpm);
    return 0;
}