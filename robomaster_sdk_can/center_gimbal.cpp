#include <iostream>

#include <can_streambuf.hpp>
#include <gimbal.hpp>


#include <chrono>
#include <thread>

#include <deque>

#include <iomanip>


int main(int, char**)
{
    auto can = can_streambuf("can0", 0x200);
    std::iostream io(&can);
    robomaster::command::gimbal gimbal(io);

    gimbal.send_workmode(1);
    gimbal.recenter();

    return 0;
}
