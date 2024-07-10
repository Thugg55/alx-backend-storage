-- Script creates a trigger that alerts; after adding an order
-- for an item it decreases the quantity of that item
CREATE TRIGGER decrease_q AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=NEW.item_name;
