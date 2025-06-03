#include <iostream>

#include <can_streambuf.hpp>
#include <gimbal.hpp>


#include <chrono>
#include <thread>

#include <deque>

#include <iomanip>

int main(int argc, char* argv[])
{
    auto can = can_streambuf("can0", 0x200);
    std::iostream io(&can);
    robomaster::command::gimbal gimbal(io);


    std::vector<int16_t> angles;
    for (int i = 1; i < argc; ++i)
    {
        std::string s = argv[i];
        angles.push_back(std::stoi(s));
    }
    int16_t yaw =angles[0];
    int16_t pitch = angles[1];
    gimbal.send_workmode(1);
    

    gimbal.send_angles(yaw, pitch);

    
    
    
    
    return 0;
}