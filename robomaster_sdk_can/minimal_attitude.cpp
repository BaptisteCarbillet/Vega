#include <iostream>
#include <array>
#include <thread>
#include <chrono>

#include <can_streambuf.hpp>
#include <protocol.hpp>     // for robomaster::package
#include <dds.hpp>          // for robomaster::dds::attitude & get_uid<>
#include <chassis.hpp>      // for robomaster::command::chassis

int main()
{
    // 1) set up CAN<->iostream
    auto can = can_streambuf("can0", 0x200);
    std::iostream io(&can);

    // 2) switch into chassis mode
    robomaster::command::chassis chassis(io);
    chassis.send_workmode(1);

    // 3) subscribe to attitude (yaw/pitch/roll) at 100 Hz = every 10 ms
    //    replace the header bytes below with the “set report” command from protocol.hpp
    robomaster::package sub_att{ /* header bytes for “set report mode” */ };
    sub_att 
      << robomaster::dds::get_uid<robomaster::dds::attitude>()  // which stream
      << uint16_t(10);                                        // period in ms
    sub_att.write_to(io);

    // 4) wait for & parse the first attitude packet
    while (true)
    {
        robomaster::package pkg;
        if (!pkg.read_from(io)) 
            continue;   // keep trying until a packet arrives

        if (pkg.uid() == robomaster::dds::get_uid<robomaster::dds::attitude>())
        {
            robomaster::dds::attitude a(pkg);
            std::cout << "Yaw:   " << a.yaw   << "°\n"
                      << "Pitch: " << a.pitch << "°\n"
                      << "Roll:  " << a.roll  << "°\n";
            break;
        }
    }

    return 0;
}