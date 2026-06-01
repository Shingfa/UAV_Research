import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    await drone.action.arm()

    # LƯỢT ĐI: Cất cánh tại A, xoay mũi sang Đông (90 độ)
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 90.0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Lỗi khởi động Offboard: {error._result.result}")
        await drone.action.disarm()
        return

    print("UAV tại Điểm A")
    await asyncio.sleep(8)

    print("Đang đến B")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 20.0, -5.0, 90.0))
    await asyncio.sleep(8)

    # Dừng Offboard để hạ cánh tự động tại Điểm B
    print("Hạ cánh tại Điểm B...")
    await drone.offboard.stop()
    await drone.action.land()

    # Chờ 10 giây để UAV tiếp đất hoàn toàn trước khi cất cánh lại
    await asyncio.sleep(8)

    # ==========================================
    # BẮT ĐẦU LƯỢT VỀ (TỪ B VỀ A)
    # ==========================================

    print("Từ B trở về A, mục đích là để test cho lần tiếp theo")
    await drone.action.arm()

    # Khóa tọa độ cất cánh tại Điểm B hiện tại (Y=20m), xoay mũi sang Tây (270 độ)
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 20.0, -5.0, 270.0))

    # Bật lại Offboard cho hành trình về
    await drone.offboard.start()

    await asyncio.sleep(8)

    print("Đang bay về A")
    # Trở về tọa độ gốc (Y=0m), mũi vẫn hướng Tây
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 270.0))
    await asyncio.sleep(8)

    print(" hạ cánh tại Điểm A...")
    await drone.offboard.stop()
    await drone.action.land()

if __name__ == "__main__":
    asyncio.run(run())
