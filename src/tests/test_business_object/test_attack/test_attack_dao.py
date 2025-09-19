from dao.attack_dao import AttackDao


class TestAttackDao:
    def test_find_attack_by_id_ok(self):
        # GIVEN
        existing_id_attack = 1

        # WHEN
        attack = AttackDao().find_attack_by_id(existing_id_attack)

        # THEN
        assert attack is not None
        assert attack.id == existing_id_attack
    
    def test_add_attack_ok(self):
       

    def test_update_attack_ok(self):

    
    