import logging


def EngineFactory(engine):
    logging.info("""EngineFactory(%s)""" % engine)

    if engine.lower() == "jinja":
        engine = 'JinjaEngine'
    else:
        engine = None

    if engine:
        return EngineInstance(engine)

    logging.error("""EngineFactory: no suitable engine found for %s""" % engine)
    return None


def EngineInstance(engine):
    if engine:
        module = __import__("docx.engines.%s" % engine, globals(), locals(), "engines")
        class_ = getattr(module, "Engine")
        instance = None
        instance = class_()
        try:
            instance = class_()
        except:
            logging.error("""EngineFactory: error while instancing %s""" % engine)
            return None
        return instance
