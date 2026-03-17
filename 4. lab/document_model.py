# public class DocumentModel {

#   public final static double SELECTION_PROXIMITY = 10;

#   // Kolekcija svih grafičkih objekata:
#   private List objects = new ArrayList<>();
#   // Read-Only proxy oko kolekcije grafičkih objekata:
#   private List roObjects = Collections.unmodifiableList(objects);
#   // Kolekcija prijavljenih promatrača:
#   private List listeners = new ArrayList<>();
#   // Kolekcija selektiranih objekata:
#   private List selectedObjects = new ArrayList<>();
#   // Read-Only proxy oko kolekcije selektiranih objekata:
#   private List roSelectedObjects = Collections.unmodifiableList(selectedObjects);

#   // Promatrač koji će biti registriran nad svim objektima crteža...
#   private final GraphicalObjectListener goListener = new GraphicalObjectListener() {...};

#   // Konstruktor...
#   public DocumentModel() {...}

#   // Brisanje svih objekata iz modela (pazite da se sve potrebno odregistrira)
#   // i potom obavijeste svi promatrači modela
#   public void clear() {...}

#   // Dodavanje objekta u dokument (pazite je li već selektiran; registrirajte model kao promatrača)
#   public void addGraphicalObject(GraphicalObject obj) {...}

#   // Uklanjanje objekta iz dokumenta (pazite je li već selektiran; odregistrirajte model kao promatrača)
#   public void removeGraphicalObject(GraphicalObject obj) {...}

#   // Vrati nepromjenjivu listu postojećih objekata (izmjene smiju ići samo kroz metode modela)
#   public List list() {...}

#   // Prijava...
#   public void addDocumentModelListener(DocumentModelListener l) {...}

#   // Odjava...
#   public void removeDocumentModelListener(DocumentModelListener l) {...}

#   // Obavještavanje...
#   public void notifyListeners() {...}

#   // Vrati nepromjenjivu listu selektiranih objekata
#   public List getSelectedObjects() {...}

#   // Pomakni predani objekt u listi objekata na jedno mjesto kasnije...
#   // Time će se on iscrtati kasnije (pa će time možda veći dio biti vidljiv)
#   public void increaseZ(GraphicalObject go) {...}

#   // Pomakni predani objekt u listi objekata na jedno mjesto ranije...
#   public void decreaseZ(GraphicalObject go) {...}

#   // Pronađi postoji li u modelu neki objekt koji klik na točku koja je
#   // predana kao argument selektira i vrati ga ili vrati null. Točka selektira
#   // objekt kojemu je najbliža uz uvjet da ta udaljenost nije veća od
#   // SELECTION_PROXIMITY. Status selektiranosti objekta ova metoda NE dira.
#   public GraphicalObject findSelectedGraphicalObject(Point mousePoint) {...}

#   // Pronađi da li u predanom objektu predana točka miša selektira neki hot-point.
#   // Točka miša selektira onaj hot-point objekta kojemu je najbliža uz uvjet da ta
#   // udaljenost nije veća od SELECTION_PROXIMITY. Vraća se indeks hot-pointa
#   // kojeg bi predana točka selektirala ili -1 ako takve nema. Status selekcije
#   // se pri tome NE dira.
#   public int findSelectedHotPoint(GraphicalObject object, Point mousePoint) {...}

# }

from typing import TYPE_CHECKING

from graphical_objects import CompositeShape, GraphicalObjectListener

if TYPE_CHECKING:
    from document_model_listener import DocumentModelListener
    from graphical_objects import EraserPath, GraphicalObject
    from point import Point


class DocumentModel(GraphicalObjectListener):
    SELECTION_PROXIMITY: float = 10

    def __init__(self):
        self._objects: list[GraphicalObject] = []
        self._z_index_objects: dict[int, list[GraphicalObject]] = {}
        self._ro_objects = tuple(self._objects)
        self._listeners: list[DocumentModelListener] = []
        self._selected_objects: list[GraphicalObject] = []
        self._ro_selected_objects = tuple(self._selected_objects)

    def clear(self):
        for obj in self.__sorted_objects():
            obj.remove_graphical_object_listener(self)
        self._objects.clear()
        self._z_index_objects.clear()
        self._ro_objects = tuple(self.__sorted_objects())
        self._selected_objects.clear()
        self._ro_selected_objects = tuple(self._selected_objects)
        self.notify_listeners()

    def add_graphical_object(self, obj: GraphicalObject):
        if obj in self.__sorted_objects():
            return

        print(f"Adding {obj} to model")
        if obj not in self.__sorted_objects():
            self._objects.append(obj)
            self._ro_objects = tuple(self.__sorted_objects())
            obj.add_graphical_object_listener(self)
            self.notify_listeners()

    def graphical_object_changed(self, go: GraphicalObject):
        self.notify_listeners()

    def graphical_object_selection_changed(self, go: GraphicalObject):
        if go.is_selected():
            if go not in self._selected_objects:
                self._selected_objects.append(go)
                self._ro_selected_objects = tuple(self._selected_objects)
        else:
            if go in self._selected_objects:
                self._selected_objects.remove(go)
                self._ro_selected_objects = tuple(self._selected_objects)
        self.notify_listeners()

    def remove_graphical_object(self, obj: GraphicalObject):
        if obj not in self.__sorted_objects():
            return

        if obj in self._objects:
            self._objects.remove(obj)
            self._ro_objects = tuple(self.__sorted_objects())
            obj.remove_graphical_object_listener(self)
        else:
            for z_index, objects in self._z_index_objects.items():
                if obj in objects:
                    objects.remove(obj)
                    obj.remove_graphical_object_listener(self)
                    if not objects:
                        del self._z_index_objects[z_index]
                    break

        if obj in self._selected_objects:
            self._selected_objects.remove(obj)
            self._ro_selected_objects = tuple(self._selected_objects)

        self.notify_listeners()

    def __sorted_objects(self):
        if not self._z_index_objects:
            yield from self._objects
            return

        need_to_yield_base_objects = True

        for z_index in sorted(self._z_index_objects.keys()):
            if z_index >= 0:
                need_to_yield_base_objects = False
                yield from self._objects
            for obj in self._z_index_objects[z_index]:
                yield obj

        if need_to_yield_base_objects:
            yield from self._objects

    def list(self):
        self._ro_objects = tuple(self.__sorted_objects())
        return self._ro_objects

    def add_document_model_listener(self, listener: DocumentModelListener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_document_model_listener(self, listener: DocumentModelListener):
        if listener in self._listeners:
            self._listeners.remove(listener)

    def notify_listeners(self):
        for listener in self._listeners:
            listener.document_change()

    def get_selected_objects(self):
        return self._ro_selected_objects

    def increase_z(self, go: GraphicalObject):
        if go not in self.__sorted_objects():
            return

        if go in self._objects:
            self._objects.remove(go)
            self._z_index_objects.setdefault(1, []).append(go)
        else:
            for z_index, objects in self._z_index_objects.items():
                if go in objects:
                    objects.remove(go)
                    if not objects:
                        del self._z_index_objects[z_index]
                    if z_index == -1:
                        self._objects.append(go)
                    else:
                        self._z_index_objects.setdefault(z_index + 1, []).append(go)
                    break

        self.notify_listeners()

    def decrease_z(self, go: GraphicalObject):
        if go not in self.__sorted_objects():
            return

        if go in self._objects:
            self._objects.remove(go)
            z_objs = self._z_index_objects.setdefault(-1, [])
            self._z_index_objects[-1] = [go, *z_objs]
        else:
            for z_index, objects in self._z_index_objects.items():
                if go in objects:
                    objects.remove(go)
                    if not objects:
                        del self._z_index_objects[z_index]
                    if z_index == 1:
                        objs = self._objects
                        self._objects = [go, *objs]
                    else:
                        z_objs = self._z_index_objects.setdefault(z_index - 1, [])
                        self._z_index_objects[z_index - 1] = [go, *z_objs]
                    break

        self.notify_listeners()

    def find_selected_graphical_object(self, mouse_point: Point):
        closest_object = None
        closest_distance = float("inf")
        for obj in list(self.__sorted_objects())[::-1]:
            distance = obj.selection_distance(mouse_point)
            if distance < closest_distance and distance <= self.SELECTION_PROXIMITY:
                closest_distance = distance
                closest_object = obj
        return closest_object

    def find_selected_hot_point(self, object: GraphicalObject, mouse_point: Point):
        closest_hot_point_index = -1
        closest_distance = float("inf")
        for i in range(object.get_number_of_hot_points()):
            distance = object.get_hot_point_distance(i, mouse_point)
            if distance == 0:
                return i
            if distance < closest_distance and distance <= self.SELECTION_PROXIMITY:
                closest_distance = distance
                closest_hot_point_index = i
        return closest_hot_point_index

    def group_selected_objects(self):
        selected_objects = self.get_selected_objects()
        print(f"Grouping selected objects: {selected_objects}")
        if len(selected_objects) <= 1:
            return

        composite = CompositeShape(selected_objects)
        for obj in selected_objects:
            obj.remove_graphical_object_listener(self)
            self.remove_graphical_object(obj)
        self.add_graphical_object(composite)
        composite.set_selected(True)
        composite.add_graphical_object_listener(self)

        self.notify_listeners()

    def ungroup_selected_objects(self):
        selected_objects = self.get_selected_objects()
        if len(selected_objects) != 1:
            return

        selected_object = selected_objects[0]
        if not isinstance(selected_object, CompositeShape):
            return

        for child in selected_object.get_shapes():
            child_copy = child.duplicate()
            self.add_graphical_object(child_copy)
            child_copy.add_graphical_object_listener(self)
            child_copy.set_selected(True)

        self.remove_graphical_object(selected_object)

        self.notify_listeners()

    def erase(self, eraser_path: EraserPath):
        points = eraser_path.get_points()
        objects_to_remove = set()

        for obj in self.__sorted_objects():
            for point in points:
                if obj.selection_distance(point) <= self.SELECTION_PROXIMITY:
                    objects_to_remove.add(obj)
                    break

        for obj in objects_to_remove:
            self.remove_graphical_object(obj)

        self.notify_listeners()
