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

    std::cout << fr_rpm << " " << fl_rpm << " " << bl_rpm << " " << br_rpm << std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    while (true)
    {
        chassis.send_heartbeat();
        chassis.send_wheel_speed(fr_rpm, fl_rpm, bl_rpm, br_rpm);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        //std::this_thread::sleep_for(std::chrono::milliseconds(1));
        //auto now = std::chrono::high_resolution_clock::now();
        //auto delta = std::chrono::duration_cast<std::chrono::milliseconds>(now - start);
        //if (delta.count() > 20)
        //{
            
        //    break;
        //}
    }
    
    
    return 0;
}