class ExcepcionBase(Exception):
    pass


class CiudadInexistenteError(ExcepcionBase):
    pass


class NoExisteCaminoError(ExcepcionBase):
    pass


class NoExisteTrayectoError(ExcepcionBase):
    pass


class NombreVacioError(ExcepcionBase):
    pass


class ParametroInvalidoError(ExcepcionBase):
    pass
