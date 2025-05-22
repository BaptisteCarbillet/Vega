#pragma once

#include <protocol.hpp>
#include <dds.hpp>
namespace robomaster
{
namespace command
{
class gimbal
{
public:
    gimbal(std::iostream& io)
        : _io{io}
    {}

    

    void send_workmode(uint8_t mode)
    {
        robomaster::package pkg{0x09, 0x04, 0x4, 0x4c, false, false};
        pkg << mode << 0x00;
        pkg.write_to(_io);
    }

    void recenter()
    {
        robomaster::package pkg{0xC9, 0x04, 0x3f, 0xb2, false, false,
            {
            0x00, 0x08, 0x05, 0x64, 0x00, 0x00, 0x00, 0x64, 0x00
            }
        };
        
        pkg.write_to(_io);
    }

    

private:
    std::iostream& _io;
};

}

}