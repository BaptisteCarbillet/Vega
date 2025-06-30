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


    std::vector<float> speed;
    for (int i = 1; i < argc; ++i)
    {
        std::string s = argv[i];
        speed.push_back(std::stoi(s));
    }
    float vx = speed[0];
    float vy = speed[1];
    float omega = speed[2];

    chassis.send_workmode(1);

    chassis.send_speed(vx, vy, omega);
    
    return 0;
}