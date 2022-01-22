import pynusmv  
import sys
from pynusmv_lower_interface.nusmv.enc.bdd.bdd import pick_one_state 
from pynusmv_lower_interface.nusmv.parser import parser 
from collections import deque  




specTypes = {'LTLSPEC': parser.TOK_LTLSPEC, 'CONTEXT': parser.CONTEXT,
    'IMPLIES': parser.IMPLIES, 'IFF': parser.IFF, 'OR': parser.OR, 'XOR': parser.XOR, 'XNOR': parser.XNOR,
    'AND': parser.AND, 'NOT': parser.NOT, 'ATOM': parser.ATOM, 'NUMBER': parser.NUMBER, 'DOT': parser.DOT,

    'NEXT': parser.OP_NEXT, 'OP_GLOBAL': parser.OP_GLOBAL, 'OP_FUTURE': parser.OP_FUTURE, 
    'UNTIL': parser.UNTIL,
    'EQUAL': parser.EQUAL, 'NOTEQUAL': parser.NOTEQUAL, 'LT': parser.LT, 'GT': parser.GT,
    'LE': parser.LE, 'GE': parser.GE, 'TRUE': parser.TRUEEXP, 'FALSE': parser.FALSEEXP
}

basicTypes = {parser.ATOM, parser.NUMBER, parser.TRUEEXP, parser.FALSEEXP, parser.DOT,
              parser.EQUAL, parser.NOTEQUAL, parser.LT, parser.GT, parser.LE, parser.GE}
booleanOp = {parser.AND, parser.OR, parser.XOR, parser.XNOR, parser.IMPLIES, parser.IFF}

def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''    
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            return True
    return False

def reverse_tuple(tuple):
    new_tuple = tuple[::-1]
    return new_tuple

def rewind(fsm, recur_state, set_of_post):
    set_of_post.reverse()
    print("lunghezza posts",len(set_of_post))
    path = ()
    path_obj = []
    state = recur_state

    path = (state.get_str_values() ,)
    path_obj.append(state)

    preSetBdd = fsm.pre(state)
    next_state = state
    pathSet = preSetBdd
    print("lo stato è: ", state.get_str_values())     
    if (len(set_of_post) == 1):
        if not(preSetBdd.intersection(state).is_false()):
            stateInput = fsm.get_inputs_between_states(state, next_state)
            path = path + (fsm.pick_one_inputs(stateInput).get_str_values(),)
            path = path + (state.get_str_values() ,)
    print("ultimo elemento", fsm.pick_one_state(set_of_post[len(set_of_post)-1]).get_str_values())
    for i in range(1,len(set_of_post)):

        state = fsm.pick_one_state(set_of_post[i].intersection(pathSet))
        stateInput = fsm.get_inputs_between_states(state, next_state)

        path = path + (fsm.pick_one_inputs(stateInput).get_str_values(),)
        path = path + (state.get_str_values() ,)

        path_obj.append(stateInput)
        path_obj.append(state)


        print("con input: ", fsm.pick_one_inputs(stateInput).get_str_values())
        print("lo stato è: ", state.get_str_values())

        preSetBdd = fsm.pre(state)
        next_state = state

        pathSet = preSetBdd

    path_obj.reverse()

    return reverse_tuple(path) #path_obj

def get_trace(fsm, recur, pre_reach):
   
    i=0
    for recur_state in fsm.pick_all_states(recur):
        already_posted = pynusmv.dd.BDD.false()
        set_of_post = []
        set_of_post.append(recur_state)
        print("iterazione____",i)
        i+=1
        post_state = fsm.post(recur_state)
        set_of_post.append(post_state)

        while not (post_state.is_false()):
            if not post_state.intersection(recur_state).is_false():
                return rewind(fsm, recur_state, set_of_post)

            post_state = fsm.post(post_state).intersection(pre_reach).diff(already_posted)
            set_of_post.append(post_state)
            already_posted = already_posted.union(post_state)
           
           
               
            


    # set_of_new.reverse()
    # j = 0
    # for recur_state in fsm.pick_all_states(recur):
    #     print(recur_state.get_str_values())
    #     print("iterazione: ",j)
    #     # for state in fsm.pick_all_states(recur):
    #     #     print("stati recur: ", state.get_str_values())
    #     # inserted = pynusmv.dd.BDD.false()
        
    #     trace = []
    #     state_trace = recur_state
    #     # trace.append(fsm.pick_one_state(recur))
    #     trace.append(state_trace)
    #     post_states = fsm.post(state_trace)
    #     #set_of_new.pop()
    #     #for i in range(len(set_of_new) - 1 ):
    #     #i = 0
    #     print("set_new ", len(set_of_new))
    #     for i in range(len(set_of_new)):
    #         if not (set_of_new[i].intersection(recur_state).is_false()):
    #             print("indice trovato")
    #             starting_index = i
    #             break

    #     for i in range(starting_index+1, len(set_of_new)):
    #         state_trace = post_states.intersection(set_of_new[i])

    #         for state in fsm.pick_all_states(state_trace):
    #             print("stati trovati: ", state.get_str_values())

    #         trace.append(state_trace)
    #         post_states = fsm.post(state_trace)

    #     state_trace = fsm.post(trace[-1]).intersection(recur_state)
        
    #     if not(state_trace.is_false()):
    #         trace.append(state_trace)
    #         print("ci sono")
    #         return trace
    #     j = j+1


        # while i < len(set_of_new):
        #     #state_trace = post_states.intersection(set_of_new[i+1])
        #     state_trace = post_states.intersection(set_of_new.pop())
        #     trace.append(state_trace)
        #     for state in fsm.pick_all_states(state_trace):
        #         print("stato trace: ", state.get_str_values())
        #     if checkIfDuplicates(trace):
        #         return trace
        #     post_states = fsm.post(state_trace)
        #     i+=1
        # for state in fsm.pick_all_states(fsm.post(trace[-1])):
        #     print("stati post: ", state.get_str_values())
        # state_trace = fsm.post(trace[-1]).intersection(trace[0])
        # trace.append(state_trace)
        # return trace

def check_formula(fsm, reach, spec_f, spec_g):
    #print("-"*10, "spec")
    # for state in fsm.pick_all_states(spec):
    #     print("stati spec: ", state.get_str_values())
    
    recur = reach.intersection(spec_f)
   
    i  = 0
    # while recur not empty
    while not(recur.is_false()): 
        print("iterazione ",i)

        set_of_new = []
        preReach = pynusmv.dd.BDD.false()
        new = fsm.pre(recur) 
        new = new.intersection(spec_g)
        set_of_new.append(new)
        while not(new.is_false()):
            preReach = preReach.union(new)
            # for state in fsm.pick_all_states(preReach):
            #     print("stati preReach: ", state.get_str_values())
            if (recur.intersection(preReach)).equal(recur):
                trace = get_trace(fsm, recur, preReach)
                return False, trace
                       
            new = fsm.pre(new).diff(preReach)
            new = new.intersection(spec_g)
            set_of_new.append(new)
        i = i+1
        recur = recur.intersection(preReach)
    return True, None


    
def get_reach(fsm):
    #get the set of reacheable states
    reach = fsm.init
    new = fsm.init
    
    while(not(new.is_false())):                                     
       
        new = fsm.post(new).diff(reach)
        reach = reach.union(new)

    # print("-"*10, "reach")
    # for state in fsm.pick_all_states(reach):
    #     print("stati reach (raggiugibili) ", state.get_str_values())
    return reach

def spec_to_bdd(model, spec):       
    """
    Given a formula `spec` with no temporal operators, returns a BDD equivalent to
    the formula, that is, a BDD that contains all the states of `model` that
    satisfy `spec`
    """
    bddspec = pynusmv.mc.eval_simple_expression(model, str(spec))
    return bddspec
    
def is_boolean_formula(spec):
    """
    Given a formula `spec`, checks if the formula is a boolean combination of base
    formulas with no temporal operators. 
    """
    if spec.type in basicTypes:
        return True
    if spec.type == specTypes['NOT']:
        return is_boolean_formula(spec.car)
    if spec.type in booleanOp:
        return is_boolean_formula(spec.car) and is_boolean_formula(spec.cdr)
    return False
    
def check_GF_formula(spec):
    """
    Given a formula `spec` checks if the formula is of the form GF f, where f is a 
    boolean combination of base formulas with no temporal operators.
    Returns the formula f if `spec` is in the correct form, None otherwise 
    """
    # check if formula is of type GF f_i
    if spec.type != specTypes['OP_GLOBAL']:
        return False
    spec = spec.car
    if spec.type != specTypes['OP_FUTURE']:
        return False
    if is_boolean_formula(spec.car):
        return spec.car
    else:
        return None

def parse_react(spec):
    """
    Visit the syntactic tree of the formula `spec` to check if it is a reactive formula,
    that is wether the formula is of the form
    
                    GF f -> GF g      
    
    where f and g are boolean combination of basic formulas.
    
    If `spec` is a reactive formula, the result is a pair where the first element is the 
    formula f and the second element is the formula g. If `spec` is not a reactive 
    formula, then the result is None.
    """
    # the root of a spec should be of type CONTEXT
    if spec.type != specTypes['CONTEXT']:
        return None
    # the right child of a context is the main formula
    spec = spec.cdr
    # the root of a reactive formula should be of type IMPLIES
    if spec.type != specTypes['IMPLIES']:
        return None
    # Check if lhs of the implication is a GF formula
    f_formula = check_GF_formula(spec.car)
    if f_formula == None:
        return None
    # Create the rhs of the implication is a GF formula
    g_formula = check_GF_formula(spec.cdr)
    if g_formula == None:
        return None
    return (f_formula, g_formula)

def check_react_spec(spec, fsm):
    """
    Return whether the loaded SMV model satisfies or not the GR(1) formula
    `spec`, that is, whether all executions of the model satisfies `spec`
    or not.
    """
    f,g = parse_react(spec)
    if parse_react(spec) == None:
        return None
    #new_spec = pynusmv.prop.imply(f,g)
    bddSpec_f = spec_to_bdd(fsm, f)
    bddSpec_g = spec_to_bdd(fsm, pynusmv.prop.not_(g))
    # notBddSpec_1 = spec_to_bdd(fsm, (f))
    # notBddSpec_2 = spec_to_bdd(fsm, (g))
    # bdd = pynusmv.mc.eval_ctl_spec(fsm, pynusmv.prop.not_(new_spec)) & fsm.reachable_states
    # newreal = fsm.pre(bdd)
    # satstates = fsm.pick_all_states(bdd)
    # for state in satstates:
    #     print("stati veri:",state.get_str_values())
    # for state in fsm.pick_all_states(newreal):
    #     print("stati veri new:",state.get_str_values())
    #print(fsm,pynusmv.prop.not_(new_spec))
    #notBddSpec = spec_to_bdd(fsm, pynusmv.prop.not_(new_spec))
    #print(notBddSpec)
    reach = get_reach(fsm)
    result, trace = check_formula(fsm, reach, bddSpec_f, bddSpec_g)
    return result, trace
    # if not check_formula(fsm, reach, notBddSpec_1):
    #     return True, None
    # elif check_formula(fsm, reach, notBddSpec_2):
    #     print("secondo")
    #     return True, None
    # else:
    #     return False, None

    #return pynusmv.mc.check_explain_ltl_spec(spec), 

# if len(sys.argv) != 2:
#     print("Usage:", sys.argv[0], "filename.smv")
#     sys.exit(1)

pynusmv.init.init_nusmv()
filename = sys.argv[1]
#filename = 'example/3bit_counter.smv'
pynusmv.glob.load_from_file(filename)
pynusmv.glob.compute_model()
fsm = pynusmv.glob.prop_database().master.bddFsm
type_ltl = pynusmv.prop.propTypes['LTL']
for prop in pynusmv.glob.prop_database():
    print()
    print("-"*100)
    print()
    spec = prop.expr
    print(spec)
    if prop.type != type_ltl:
        print("property is not LTLSPEC, skipping")
        continue
    res = check_react_spec(spec, fsm)
    if res == None:
        print('Property is not a GR(1) formula, skipping')
    if res[0] == True:
        print("Property is respected")
    elif res[0] == False:
        print("trace")
        print(res[1])
        #for state in res[1]:
           #print(fsm.pick_one_state(state).get_str_values())
        print("Property is not respected")
        #print("Counterexample:", res[1])

    print(pynusmv.mc.check_explain_ltl_spec(spec))
   


pynusmv.init.deinit_nusmv()


# - recuperato f e g separatamente con parse_react (escludendo quindi gli operatore temporali)
# - unite con la funzione  "imply" (abbiamo anche provato ad eseguire f e g separatamente e fare l'imply dopo)
# - negato la formula e creato il bdd corrispondente
# - usato l´ algoritmo symbolic repeatedly_check sulla formula negata per controllare se la formula negata é true (proprietá non rispettata) o false (proprietá rispettata) 
# - Hai seguito anche te lo stesso procedimento? Oppure abbiamo perso qualcosa?
