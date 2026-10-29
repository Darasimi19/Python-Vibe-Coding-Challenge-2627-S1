import tkinter as tk
import random


class WastelandChef:
    def __init__(self, root):
        self.root = root
        self.root.title("Wasteland Chef: Survive the Shift")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack()

        # Survival Game State
        self.rations = 0
        self.health = 3
        self.game_over = False
        self.ingredients_list = ["Rad-Tomato", "Scrap Meat", "Swamp Weed", "Mutant Shroom"]
        self.current_order = []
        self.pot_contents = []

        # New robust drag system
        self.drag_item_name = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.ingredient_data = {}

        # Mutant Animation State
        self.customer_state = "entering"
        self.customer_x = 850
        self.mutant_skin_colors = ["#81c784", "#aed581", "#78909c", "#bcaaa4"]

        self.draw_environment()
        self.setup_game_objects()

        # Bind Mouse Events
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_drag_stop)

        # Start game loop
        self.update_animation()

    def draw_environment(self):
        # 1. Wasteland Background
        self.canvas.create_rectangle(0, 0, 800, 300, fill="#263238", outline="")

        # 2. Mutant Customer
        self.cust_body = self.canvas.create_rectangle(840, 210, 920, 350, fill="#5d4037", outline="")
        self.cust_head = self.canvas.create_oval(845, 140, 915, 215, fill="#81c784", outline="")
        self.cust_eye = self.canvas.create_oval(865, 160, 895, 190, fill="#ff5252", outline="black")

        # 3. Rusty Metal Counter & Scrap Shelf
        self.canvas.create_rectangle(0, 300, 800, 600, fill="#4e342e", outline="")
        self.canvas.create_rectangle(0, 300, 800, 310, fill="#3e2723", outline="")
        self.canvas.create_rectangle(50, 420, 750, 435, fill="#546e7a", outline="")

        # 4. Survivor UI Overlay
        self.canvas.create_rectangle(25, 25, 255, 155, fill="#37474f", outline="#212121", width=3)
        self.canvas.create_text(35, 40, text="MUTANT ORDER:", font=("Consolas", 14, "bold"), anchor="w", fill="#ffeb3b")
        self.ticket_text = self.canvas.create_text(35, 80, text="Approaching...", font=("Consolas", 12, "bold"),
                                                   anchor="w", fill="#eceff1")

        self.status_text = self.canvas.create_text(400, 560, text="Survive the shift. Don't poison them.",
                                                   font=("Consolas", 14), fill="#b0bec5")
        self.rations_text = self.canvas.create_text(750, 540, text=f"Rations: {self.rations}",
                                                    font=("Consolas", 16, "bold"), anchor="e", fill="#4caf50")
        self.health_text = self.canvas.create_text(750, 570, text=f"Health: {'♥' * self.health}",
                                                   font=("Consolas", 16, "bold"), anchor="e", fill="#f44336")

    def setup_game_objects(self):
        self.pot_id = self.canvas.create_oval(150, 180, 350, 280, fill="#3e2723", outline="#212121", width=4)
        self.canvas.create_oval(170, 195, 330, 265, fill="#64dd17", outline="")

        ingredients = [
            ("Rad-Tomato", 260, 450, "#ff1744"),
            ("Scrap Meat", 380, 450, "#795548"),
            ("Swamp Weed", 500, 450, "#00e676"),
            ("Mutant Shroom", 620, 450, "#d500f9")
        ]

        for name, x, y, color in ingredients:
            # We give both the shape and the text a specific tag (item_Name) so they link together
            unique_tag = f"item_{name}"
            shape_id = self.canvas.create_oval(x - 35, y - 35, x + 35, y + 35, fill=color, outline="#111", width=2,
                                               tags=("draggable", unique_tag))
            text_id = self.canvas.create_text(x, y - 50, text=name, font=("Consolas", 11, "bold"), fill="#cfd8dc",
                                              tags=("draggable", unique_tag))

            self.ingredient_data[name] = {
                "shape_id": shape_id,
                "text_id": text_id,
                "start_x": x - 35,
                "start_y": y - 35,
                "tag": unique_tag
            }

    def update_animation(self):
        if self.game_over:
            return

        if self.customer_state == "entering":
            if self.customer_x > 500:
                self.move_mutant(-6)
            else:
                self.customer_state = "waiting"
                self.generate_new_order()

        elif self.customer_state == "leaving":
            if self.customer_x > -150:
                self.move_mutant(-8)
            else:
                self.spawn_new_customer()

        self.root.after(16, self.update_animation)

    def move_mutant(self, dx):
        self.canvas.move(self.cust_head, dx, 0)
        self.canvas.move(self.cust_body, dx, 0)
        self.canvas.move(self.cust_eye, dx, 0)
        self.customer_x += dx

    def spawn_new_customer(self):
        self.customer_x = 850
        self.canvas.coords(self.cust_head, 845, 140, 915, 215)
        self.canvas.coords(self.cust_body, 840, 210, 920, 350)
        self.canvas.coords(self.cust_eye, 865, 160, 895, 190)

        self.canvas.itemconfig(self.cust_head, fill=random.choice(self.mutant_skin_colors))
        self.canvas.itemconfig(self.ticket_text, text="Approaching...")
        self.canvas.itemconfig(self.status_text, text="A survivor approaches...", fill="#b0bec5")
        self.customer_state = "entering"

    def generate_new_order(self):
        self.pot_contents = []
        num_items = random.choice([2, 3])
        self.current_order = random.sample(self.ingredients_list, num_items)
        self.canvas.itemconfig(self.ticket_text, text=f"Feed me:\n{', '.join(self.current_order)}")
        self.canvas.itemconfig(self.status_text, text="Don't mess this up.", fill="#ffeb3b")

    def get_item_name_from_tags(self, tags):
        for tag in tags:
            if tag.startswith("item_"):
                return tag.replace("item_", "")
        return None

    def on_drag_start(self, event):
        if self.game_over: return

        items = self.canvas.find_withtag("current")
        if not items: return

        clicked_item = items[0]
        tags = self.canvas.gettags(clicked_item)

        self.drag_item_name = self.get_item_name_from_tags(tags)
        if self.drag_item_name:
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # Bring both shape and text to front
            data = self.ingredient_data[self.drag_item_name]
            self.canvas.tag_raise(data["shape_id"])
            self.canvas.tag_raise(data["text_id"])

    def on_drag_motion(self, event):
        if self.drag_item_name and not self.game_over:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            # Move both pieces together using their shared tag
            tag = self.ingredient_data[self.drag_item_name]["tag"]
            self.canvas.move(tag, dx, dy)

            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def check_collision(self, item_name, target_id):
        shape_id = self.ingredient_data[item_name]["shape_id"]
        b1 = self.canvas.bbox(shape_id)
        b2 = self.canvas.bbox(target_id)
        if not b1 or not b2: return False
        return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])

    def trigger_game_over(self):
        self.game_over = True
        self.canvas.itemconfig(self.status_text, text="GAME OVER! The wasteland claimed you.", fill="#ff5252",
                               font=("Consolas", 18, "bold"))
        self.canvas.itemconfig(self.ticket_text, text="DEAD")

    def on_drag_stop(self, event):
        if self.drag_item_name and not self.game_over:
            name = self.drag_item_name

            if self.customer_state == "waiting" and self.check_collision(name, self.pot_id):
                if name in self.current_order and name not in self.pot_contents:
                    self.pot_contents.append(name)
                    self.canvas.itemconfig(self.status_text, text=f"Tossed in {name}.", fill="#64dd17")
                else:
                    self.health -= 1
                    self.canvas.itemconfig(self.health_text, text=f"Health: {'♥' * self.health}")
                    if self.health <= 0:
                        self.trigger_game_over()
                    else:
                        self.canvas.itemconfig(self.status_text, text=f"WRONG INGREDIENT! They attacked you!",
                                               fill="#ff5252")

                if len(self.pot_contents) == len(self.current_order) and not self.game_over:
                    self.rations += 15
                    self.canvas.itemconfig(self.rations_text, text=f"Rations: {self.rations}")
                    self.canvas.itemconfig(self.status_text, text="Mutant fed. Surviving another day.", fill="#64dd17")
                    self.canvas.itemconfig(self.ticket_text, text="...")
                    self.customer_state = "leaving"

            self.reset_item_position(name)
            self.drag_item_name = None

    def reset_item_position(self, name):
        data = self.ingredient_data[name]
        current_bbox = self.canvas.bbox(data["shape_id"])
        if not current_bbox: return

        dx = data["start_x"] - current_bbox[0]
        dy = data["start_y"] - current_bbox[1]

        self.canvas.move(data["tag"], dx, dy)


if __name__ == "__main__":
    root = tk.Tk()
    app = WastelandChef(root)
    root.mainloop()