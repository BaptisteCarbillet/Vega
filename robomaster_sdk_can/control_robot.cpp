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
        speed.push_back(std::stof(s));
    }
    float vx = speed[0];
    float vy = speed[1];
    float omega = speed[2];
    float timeout = speed[3];
    chassis.send_workmode(1);
    std::cout << "Setting speed: vx=" << vx << ", vy=" << vy << ", omega=" << omega << std::endl;
    //while (true)
    //{
    //    chassis.send_heartbeat();
     //   chassis.send_speed(vx, vy, omega);
      //  std::this_thread::sleep_for(std::chrono::milliseconds(10));
    //}
    //write same loop but instead of while true do while time < timeout

    auto start = std::chrono::steady_clock::now();
    while (std::chrono::steady_clock::now() - start < std::chrono::seconds(static_cast<int>(timeout)))
    {
        chassis.send_heartbeat();
        chassis.send_speed(vx, vy, omega);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    
    return 0;
}