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

from graphical_objects.listener import GraphicalObjectListener

if TYPE_CHECKING:
    from document_model_listener import DocumentModelListener
    from graphical_objects.interface import GraphicalObject
    from point import Point


class DocumentModel(GraphicalObjectListener):
    SELECTION_PROXIMITY: float = 10

    def __init__(self):
        self._objects = []
        self._ro_objects = tuple(self._objects)
        self._listeners = []
        self._selected_objects = []
        self._ro_selected_objects = tuple(self._selected_objects)

    def clear(self): ...

    def add_graphical_object(self, obj: GraphicalObject):
        print(f"Adding {obj} to model")
        if obj not in self._objects:
            self._objects.append(obj)
            self._ro_objects = tuple(self._objects)
            obj.add_graphical_object_listener(self)
            self.notify_listeners()

    def graphical_object_changed(self, go: GraphicalObject):
        print(f"Graphical object changed: {go}")
        self.notify_listeners()

    def graphical_object_selection_changed(self, go: GraphicalObject): ...

    def remove_graphical_object(self, obj: GraphicalObject): ...

    def list(self):
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

    def get_selected_objects(self): ...

    def increase_z(self, go: GraphicalObject): ...

    def decrease_z(self, go: GraphicalObject): ...

    def find_selected_graphical_object(self, mouse_point: Point): ...

    def find_selected_hot_point(self, object: GraphicalObject, mouse_point: Point): ...
