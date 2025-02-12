import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleMovementTestNode(Node):
    def __init__(self):
        super().__init__('simple_movement_test_node')
        self.publisher = self.create_publisher(String, 'comandi_movimento', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)  # Pubblica ogni 2 secondi
        self.commands = ["avanti", "indietro", "sinistra", "destra"]
        self.current_command_index = 0

    def timer_callback(self):
        # Pubblica il comando corrente
        comando = self.commands[self.current_command_index]
        self.get_logger().info(f'Pubblicando comando: "{comando}"')
        msg = String()
        msg.data = comando
        self.publisher.publish(msg)

        # Aggiorna l'indice del comando
        self.current_command_index += 1
        if self.current_command_index >= len(self.commands):
            self.current_command_index = 0  # Ripeti il ciclo

def main(args=None):
    rclpy.init(args=args)
    node = SimpleMovementTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
